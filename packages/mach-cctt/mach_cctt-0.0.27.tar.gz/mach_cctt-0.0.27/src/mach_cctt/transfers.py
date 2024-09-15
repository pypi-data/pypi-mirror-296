import logging
from pprint import pformat

from mach_client import client, Token
from web3 import AsyncWeb3
from web3.types import TxParams
from web3._utils.async_transactions import (
    async_fill_nonce,
    async_fill_transaction_defaults,
)

from .utility import make_token_contract


logger = logging.getLogger("cctt")


async def fill_transaction_defaults(w3: AsyncWeb3, transaction: TxParams) -> TxParams:
    transaction = await async_fill_nonce(w3, transaction)
    return await async_fill_transaction_defaults(w3, transaction)


async def send_transaction(
    w3: AsyncWeb3, private_key, transaction: TxParams, identifier: str
) -> None:
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
    transaction_hash = await w3.eth.send_raw_transaction(
        signed_transaction.raw_transaction
    )

    logger.info(f"Hash for {identifier}: {transaction_hash.hex()}")

    transaction_receipt = await w3.eth.wait_for_transaction_receipt(transaction_hash)

    logger.info(f"Received receipt for {identifier}:")
    logger.info(pformat(dict(transaction_receipt)))

    if transaction_receipt["status"] != 0x1:
        raise RuntimeError(f"{identifier} transaction failed")

    logger.info(f"Transaction success for {identifier}")


async def transfer_token(
    w3: AsyncWeb3, token: Token, amount: int, public_key, private_key, wallet
) -> None:
    assert (
        client.gas_tokens[token.chain.id] != token.symbol
    ), "Token must be ERC-20 token, not gas token"

    if amount <= 0:
        logger.info(f"Skipping {token} - balance empty")
        return

    logger.info(f"Transferring {amount} units of {token}")

    contract = make_token_contract(w3, token)

    params = await async_fill_transaction_defaults(
        w3,
        {
            "chainId": token.chain.id,
            "from": public_key,
        },
    )

    transaction = await contract.functions.transfer(wallet, amount).build_transaction(
        params
    )

    await send_transaction(w3, private_key, transaction, str(token))
