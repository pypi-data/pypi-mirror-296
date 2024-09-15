import asyncio
import logging
from pprint import pformat

from mach_client import ChainId, client, Token
from web3 import AsyncWeb3
from web3.types import Wei
from web3.middleware import ExtraDataToPOAMiddleware

from .transfers import fill_transaction_defaults, send_transaction, transfer_token


logger = logging.getLogger("cctt")


async def drain_gas(w3: AsyncWeb3, public_key, private_key, wallet) -> None:
    chain = ChainId(await w3.eth.chain_id)
    logger.info(f"Withdrawing {chain} gas")

    # TODO: This does not currently account for L1 fees for Optimism, which will thus fail
    # https://docs.optimism.io/stack/transactions/fees
    # https://github.com/ethereum/web3.py/issues/3079

    transaction = await fill_transaction_defaults(
        w3,
        {
            "from": public_key,
            "to": wallet,
        },
    )

    gas = transaction["gas"]  # type: ignore
    max_fee_per_gas: Wei = transaction["maxFeePerGas"]  # type: ignore
    total_gas_cost = w3.to_wei(gas * max_fee_per_gas, "wei")

    balance = await w3.eth.get_balance(public_key)
    value = w3.to_wei(max(0, balance - total_gas_cost), "wei")

    logger.debug(f"{chain} gas balance of {balance}")
    logger.debug(f"{chain} gas of {gas}")
    logger.debug(f"{chain} max fee per gas of {max_fee_per_gas}")
    logger.debug(f"{chain} total gas cost of {total_gas_cost}")
    logger.debug(f"{chain} transaction value would be {value}")

    if value <= 0:
        logger.info(f"Skipping gas on {chain}, balance of 0")
        return

    transaction["value"] = value

    await send_transaction(w3, private_key, transaction, f"{chain} gas")


# Drains balances of all tokens and gas asset on the chain into the destination wallet
async def drain_chain(
    chain: ChainId, balances: dict[str, int], public_key, private_key, wallet
) -> None:
    logger.info(f"Draining {chain}")

    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(client.rpc_urls[chain]))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    gas_token = client.gas_tokens[chain]

    # First drain everything but the gas token
    await asyncio.gather(
        *(
            transfer_token(
                w3,
                Token.from_components(chain, symbol),
                balance,
                public_key,
                private_key,
                wallet,
            )
            for symbol, balance in filter(
                lambda item: item[0] != gas_token, balances.items()
            )
        )
    )

    # Then drain the gas token
    try:
        await drain_gas(w3, public_key, private_key, wallet)
    except Exception as e:
        logging.warning(f"Failed to withdraw gas ok {chain}: {e}")


async def drain_all(public_key, private_key, wallet) -> None:
    all_balances = client.get_token_balances(public_key)

    logger.info("Balances:")
    logger.info(pformat(all_balances))

    await asyncio.gather(
        *(
            drain_chain(chain, balances, public_key, private_key, wallet)
            for chain, balances in all_balances.items()
        )
    )
