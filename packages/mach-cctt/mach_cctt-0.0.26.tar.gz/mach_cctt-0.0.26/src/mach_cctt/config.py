# Time to wait between polls of the destination balance to check if the desired amount has been received
poll_timeout = 10

# Maximum number of polls
max_polls = 30

log_files = {
    # Source funds not withdrawn
    "delayed_transactions": "delayed_transactions.log",
    # Source funds withdrawn, destination funds not received
    "stuck_transactions": "stuck_transactions.log",
    # Filled for less than order was placed for or received less than order was quoted for
    "improper_fills": "improper_fills.log",
}

order_book_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "_endpoint", "type": "address"},
            {"internalType": "address", "name": "_owner", "type": "address"},
            {"internalType": "uint32", "name": "_lzEid", "type": "uint32"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {"inputs": [], "name": "InvalidDelegate", "type": "error"},
    {"inputs": [], "name": "InvalidEndpointCall", "type": "error"},
    {
        "inputs": [{"internalType": "bytes", "name": "options", "type": "bytes"}],
        "name": "InvalidOptions",
        "type": "error",
    },
    {"inputs": [], "name": "LzTokenUnavailable", "type": "error"},
    {
        "inputs": [{"internalType": "uint32", "name": "eid", "type": "uint32"}],
        "name": "NoPeer",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "msgValue", "type": "uint256"}],
        "name": "NotEnoughNative",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "addr", "type": "address"}],
        "name": "OnlyEndpoint",
        "type": "error",
    },
    {
        "inputs": [
            {"internalType": "uint32", "name": "eid", "type": "uint32"},
            {"internalType": "bytes32", "name": "sender", "type": "bytes32"},
        ],
        "name": "OnlyPeer",
        "type": "error",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "challenger",
                "type": "address",
            },
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "indexed": False,
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "srcIndex",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "bonder",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "dstIndex",
                "type": "uint32",
            },
        ],
        "name": "ChallengeRaised",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bool",
                "name": "challenge_status",
                "type": "bool",
            }
        ],
        "name": "ChallengeResult",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "components": [
                    {"internalType": "uint32", "name": "eid", "type": "uint32"},
                    {"internalType": "uint16", "name": "msgType", "type": "uint16"},
                    {"internalType": "bytes", "name": "options", "type": "bytes"},
                ],
                "indexed": False,
                "internalType": "struct EnforcedOptionParam[]",
                "name": "_enforcedOptions",
                "type": "tuple[]",
            }
        ],
        "name": "EnforcedOptionSet",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "bonder",
                "type": "address",
            },
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "indexed": False,
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "srcIndex",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "dstIndex",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "bondFee",
                "type": "uint16",
            },
        ],
        "name": "MatchConfirmed",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "bonder",
                "type": "address",
            },
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "indexed": False,
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "srcIndex",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "dstIndex",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "uint96",
                "name": "srcQuantity",
                "type": "uint96",
            },
            {
                "indexed": False,
                "internalType": "uint96",
                "name": "dstQuantity",
                "type": "uint96",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "Maker",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint96",
                "name": "blockNumber",
                "type": "uint96",
            },
        ],
        "name": "MatchCreated",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "bonder",
                "type": "address",
            },
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "indexed": False,
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "srcIndex",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "dstIndex",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "uint96",
                "name": "srcQuantity",
                "type": "uint96",
            },
            {
                "indexed": False,
                "internalType": "uint96",
                "name": "dstQuantity",
                "type": "uint96",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "Taker",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "isWrapped",
                "type": "bool",
            },
        ],
        "name": "MatchExecuted",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "bonder",
                "type": "address",
            },
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "indexed": False,
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "srcIndex",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "dstIndex",
                "type": "uint32",
            },
        ],
        "name": "MatchUnwound",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "string",
                "name": "message",
                "type": "string",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "senderEid",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "sender",
                "type": "bytes32",
            },
        ],
        "name": "MessageReceived",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "message",
                "type": "bytes",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "dstEid",
                "type": "uint32",
            },
        ],
        "name": "MessageSent",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address",
            },
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "indexed": False,
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "orderIndex",
                "type": "uint32",
            },
        ],
        "name": "OrderCancelled",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "orderIndex",
                "type": "uint32",
            },
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "indexed": False,
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "uint96", "name": "srcQuantity", "type": "uint96"},
                    {"internalType": "uint96", "name": "dstQuantity", "type": "uint96"},
                    {"internalType": "uint16", "name": "bondFee", "type": "uint16"},
                    {"internalType": "address", "name": "bondAsset", "type": "address"},
                    {"internalType": "uint96", "name": "bondAmount", "type": "uint96"},
                ],
                "indexed": False,
                "internalType": "struct TradeInterface.OrderFunding",
                "name": "funding",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "uint32", "name": "timestamp", "type": "uint32"},
                    {
                        "internalType": "uint16",
                        "name": "challengeOffset",
                        "type": "uint16",
                    },
                    {
                        "internalType": "uint16",
                        "name": "challengeWindow",
                        "type": "uint16",
                    },
                ],
                "indexed": False,
                "internalType": "struct TradeInterface.OrderExpiration",
                "name": "expiration",
                "type": "tuple",
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "isMaker",
                "type": "bool",
            },
        ],
        "name": "OrderPlaced",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnershipTransferred",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "eid",
                "type": "uint32",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "peer",
                "type": "bytes32",
            },
        ],
        "name": "PeerSet",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "string",
                "name": "message",
                "type": "string",
            },
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "dstEid",
                "type": "uint32",
            },
        ],
        "name": "ReturnMessageSent",
        "type": "event",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "uint32", "name": "srcEid", "type": "uint32"},
                    {"internalType": "bytes32", "name": "sender", "type": "bytes32"},
                    {"internalType": "uint64", "name": "nonce", "type": "uint64"},
                ],
                "internalType": "struct Origin",
                "name": "origin",
                "type": "tuple",
            }
        ],
        "name": "allowInitializePath",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "number", "type": "uint256"},
            {"internalType": "uint256", "name": "_fee", "type": "uint256"},
        ],
        "name": "applyFee",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "number", "type": "uint256"},
            {"internalType": "uint256", "name": "_fee", "type": "uint256"},
        ],
        "name": "bondFee",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "address", "name": "", "type": "address"},
        ],
        "name": "book",
        "outputs": [
            {"internalType": "address", "name": "src", "type": "address"},
            {"internalType": "address", "name": "dst", "type": "address"},
            {"internalType": "uint16", "name": "lzc", "type": "uint16"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {"internalType": "uint32", "name": "orderIndex", "type": "uint32"},
        ],
        "name": "cancelOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {"internalType": "uint32", "name": "srcIndex", "type": "uint32"},
            {"internalType": "bytes", "name": "_extraSendOptions", "type": "bytes"},
            {"internalType": "bytes", "name": "_extraReturnOptions", "type": "bytes"},
        ],
        "name": "challengeMatch",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint32", "name": "_eid", "type": "uint32"},
            {"internalType": "uint16", "name": "_msgType", "type": "uint16"},
            {"internalType": "bytes", "name": "_extraOptions", "type": "bytes"},
        ],
        "name": "combineOptions",
        "outputs": [{"internalType": "bytes", "name": "", "type": "bytes"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {"internalType": "uint32", "name": "srcIndex", "type": "uint32"},
        ],
        "name": "confirmMatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {"internalType": "uint32", "name": "srcIndex", "type": "uint32"},
            {"internalType": "uint32", "name": "dstIndex", "type": "uint32"},
            {"internalType": "address", "name": "Counterparty", "type": "address"},
            {"internalType": "uint96", "name": "srcQuantity", "type": "uint96"},
            {"internalType": "uint96", "name": "dstQuantity", "type": "uint96"},
        ],
        "name": "createMatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes", "name": "encodedMessage", "type": "bytes"}
        ],
        "name": "decodeMessage",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "challenger",
                        "type": "address",
                    },
                    {"internalType": "uint32", "name": "srcLzc", "type": "uint32"},
                    {"internalType": "address", "name": "srcToken", "type": "address"},
                    {"internalType": "address", "name": "dstToken", "type": "address"},
                    {"internalType": "uint32", "name": "srcIndex", "type": "uint32"},
                    {"internalType": "uint32", "name": "dstIndex", "type": "uint32"},
                    {"internalType": "address", "name": "taker", "type": "address"},
                    {"internalType": "uint256", "name": "minAmount", "type": "uint256"},
                    {"internalType": "uint256", "name": "status", "type": "uint256"},
                ],
                "internalType": "struct TradeInterface.Payload",
                "name": "message",
                "type": "tuple",
            },
            {"internalType": "uint16", "name": "msgType", "type": "uint16"},
            {"internalType": "uint256", "name": "extraOptionsStart", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "extraOptionsLength",
                "type": "uint256",
            },
        ],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "endpoint",
        "outputs": [
            {
                "internalType": "contract ILayerZeroEndpointV2",
                "name": "",
                "type": "address",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint32", "name": "eid", "type": "uint32"},
            {"internalType": "uint16", "name": "msgType", "type": "uint16"},
        ],
        "name": "enforcedOptions",
        "outputs": [
            {"internalType": "bytes", "name": "enforcedOption", "type": "bytes"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {"internalType": "uint32", "name": "srcIndex", "type": "uint32"},
            {"internalType": "uint32", "name": "dstIndex", "type": "uint32"},
            {"internalType": "address", "name": "Counterparty", "type": "address"},
            {"internalType": "uint96", "name": "srcQuantity", "type": "uint96"},
            {"internalType": "uint96", "name": "dstQuantity", "type": "uint96"},
            {"internalType": "bool", "name": "isUnwrap", "type": "bool"},
        ],
        "name": "executeMatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getCurrentBlockNumber",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "srcAsset", "type": "address"},
            {"internalType": "address", "name": "dstAsset", "type": "address"},
            {"internalType": "uint256", "name": "dstLzc", "type": "uint256"},
            {"internalType": "uint256", "name": "index", "type": "uint256"},
        ],
        "name": "getMatch",
        "outputs": [
            {
                "components": [
                    {"internalType": "uint32", "name": "dstIndex", "type": "uint32"},
                    {"internalType": "uint96", "name": "srcQuantity", "type": "uint96"},
                    {"internalType": "uint96", "name": "dstQuantity", "type": "uint96"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "bonder", "type": "address"},
                    {"internalType": "uint96", "name": "blockNumber", "type": "uint96"},
                    {"internalType": "bool", "name": "finalized", "type": "bool"},
                    {"internalType": "bool", "name": "challenged", "type": "bool"},
                ],
                "internalType": "struct TradeInterface.Match",
                "name": "_match",
                "type": "tuple",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "srcAsset", "type": "address"},
            {"internalType": "address", "name": "dstAsset", "type": "address"},
            {"internalType": "uint256", "name": "dstLzc", "type": "uint256"},
            {"internalType": "uint256", "name": "index", "type": "uint256"},
        ],
        "name": "getOrder",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {
                        "components": [
                            {
                                "internalType": "uint96",
                                "name": "srcQuantity",
                                "type": "uint96",
                            },
                            {
                                "internalType": "uint96",
                                "name": "dstQuantity",
                                "type": "uint96",
                            },
                            {
                                "internalType": "uint16",
                                "name": "bondFee",
                                "type": "uint16",
                            },
                            {
                                "internalType": "address",
                                "name": "bondAsset",
                                "type": "address",
                            },
                            {
                                "internalType": "uint96",
                                "name": "bondAmount",
                                "type": "uint96",
                            },
                        ],
                        "internalType": "struct TradeInterface.OrderFunding",
                        "name": "funding",
                        "type": "tuple",
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "timestamp",
                                "type": "uint32",
                            },
                            {
                                "internalType": "uint16",
                                "name": "challengeOffset",
                                "type": "uint16",
                            },
                            {
                                "internalType": "uint16",
                                "name": "challengeWindow",
                                "type": "uint16",
                            },
                        ],
                        "internalType": "struct TradeInterface.OrderExpiration",
                        "name": "expiration",
                        "type": "tuple",
                    },
                    {"internalType": "uint96", "name": "settled", "type": "uint96"},
                    {"internalType": "bool", "name": "isMaker", "type": "bool"},
                ],
                "internalType": "struct TradeInterface.Order",
                "name": "_order",
                "type": "tuple",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "srcAsset", "type": "address"},
            {"internalType": "address", "name": "dstAsset", "type": "address"},
            {"internalType": "uint256", "name": "dstLzc", "type": "uint256"},
        ],
        "name": "getOrders",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {
                        "components": [
                            {
                                "internalType": "uint96",
                                "name": "srcQuantity",
                                "type": "uint96",
                            },
                            {
                                "internalType": "uint96",
                                "name": "dstQuantity",
                                "type": "uint96",
                            },
                            {
                                "internalType": "uint16",
                                "name": "bondFee",
                                "type": "uint16",
                            },
                            {
                                "internalType": "address",
                                "name": "bondAsset",
                                "type": "address",
                            },
                            {
                                "internalType": "uint96",
                                "name": "bondAmount",
                                "type": "uint96",
                            },
                        ],
                        "internalType": "struct TradeInterface.OrderFunding",
                        "name": "funding",
                        "type": "tuple",
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "timestamp",
                                "type": "uint32",
                            },
                            {
                                "internalType": "uint16",
                                "name": "challengeOffset",
                                "type": "uint16",
                            },
                            {
                                "internalType": "uint16",
                                "name": "challengeWindow",
                                "type": "uint16",
                            },
                        ],
                        "internalType": "struct TradeInterface.OrderExpiration",
                        "name": "expiration",
                        "type": "tuple",
                    },
                    {"internalType": "uint96", "name": "settled", "type": "uint96"},
                    {"internalType": "bool", "name": "isMaker", "type": "bool"},
                ],
                "internalType": "struct TradeInterface.Order[]",
                "name": "orders",
                "type": "tuple[]",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "srcAsset", "type": "address"},
            {"internalType": "address", "name": "dstAsset", "type": "address"},
            {"internalType": "uint256", "name": "dstLzc", "type": "uint256"},
            {"internalType": "uint256", "name": "srcIndex", "type": "uint256"},
            {"internalType": "uint256", "name": "dstIndex", "type": "uint256"},
        ],
        "name": "getReceipt",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint96",
                        "name": "payoutQuantity",
                        "type": "uint96",
                    },
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "internalType": "struct TradeInterface.Receipt",
                "name": "_receipt",
                "type": "tuple",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "uint32", "name": "srcEid", "type": "uint32"},
                    {"internalType": "bytes32", "name": "sender", "type": "bytes32"},
                    {"internalType": "uint64", "name": "nonce", "type": "uint64"},
                ],
                "internalType": "struct Origin",
                "name": "",
                "type": "tuple",
            },
            {"internalType": "bytes", "name": "", "type": "bytes"},
            {"internalType": "address", "name": "_sender", "type": "address"},
        ],
        "name": "isComposeMsgSender",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "uint32", "name": "srcEid", "type": "uint32"},
                    {"internalType": "bytes32", "name": "sender", "type": "bytes32"},
                    {"internalType": "uint64", "name": "nonce", "type": "uint64"},
                ],
                "internalType": "struct Origin",
                "name": "_origin",
                "type": "tuple",
            },
            {"internalType": "bytes32", "name": "_guid", "type": "bytes32"},
            {"internalType": "bytes", "name": "_message", "type": "bytes"},
            {"internalType": "address", "name": "_executor", "type": "address"},
            {"internalType": "bytes", "name": "_extraData", "type": "bytes"},
        ],
        "name": "lzReceive",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "maxFee",
        "outputs": [{"internalType": "uint16", "name": "", "type": "uint16"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint32", "name": "", "type": "uint32"},
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
        ],
        "name": "nextNonce",
        "outputs": [{"internalType": "uint64", "name": "nonce", "type": "uint64"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "oAppVersion",
        "outputs": [
            {"internalType": "uint64", "name": "senderVersion", "type": "uint64"},
            {"internalType": "uint64", "name": "receiverVersion", "type": "uint64"},
        ],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint32", "name": "eid", "type": "uint32"}],
        "name": "peers",
        "outputs": [{"internalType": "bytes32", "name": "peer", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "uint96", "name": "srcQuantity", "type": "uint96"},
                    {"internalType": "uint96", "name": "dstQuantity", "type": "uint96"},
                    {"internalType": "uint16", "name": "bondFee", "type": "uint16"},
                    {"internalType": "address", "name": "bondAsset", "type": "address"},
                    {"internalType": "uint96", "name": "bondAmount", "type": "uint96"},
                ],
                "internalType": "struct TradeInterface.OrderFunding",
                "name": "funding",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "uint32", "name": "timestamp", "type": "uint32"},
                    {
                        "internalType": "uint16",
                        "name": "challengeOffset",
                        "type": "uint16",
                    },
                    {
                        "internalType": "uint16",
                        "name": "challengeWindow",
                        "type": "uint16",
                    },
                ],
                "internalType": "struct TradeInterface.OrderExpiration",
                "name": "expiration",
                "type": "tuple",
            },
            {"internalType": "bool", "name": "isMaker", "type": "bool"},
        ],
        "name": "placeOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "_delegate", "type": "address"}],
        "name": "setDelegate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "uint32", "name": "eid", "type": "uint32"},
                    {"internalType": "uint16", "name": "msgType", "type": "uint16"},
                    {"internalType": "bytes", "name": "options", "type": "bytes"},
                ],
                "internalType": "struct EnforcedOptionParam[]",
                "name": "_enforcedOptions",
                "type": "tuple[]",
            }
        ],
        "name": "setEnforcedOptions",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint16", "name": "_newMaxFee", "type": "uint16"}],
        "name": "setMaxFee",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint32", "name": "_eid", "type": "uint32"},
            {"internalType": "bytes32", "name": "_peer", "type": "bytes32"},
        ],
        "name": "setPeer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "srcLzc",
        "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "srcAsset", "type": "address"},
                    {"internalType": "address", "name": "dstAsset", "type": "address"},
                    {"internalType": "uint32", "name": "dstLzc", "type": "uint32"},
                ],
                "internalType": "struct TradeInterface.OrderDirection",
                "name": "direction",
                "type": "tuple",
            },
            {"internalType": "uint32", "name": "srcIndex", "type": "uint32"},
        ],
        "name": "unwindMatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {"stateMutability": "payable", "type": "receive"},
]

erc20_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "_upgradedAddress", "type": "address"}],
        "name": "deprecate",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "deprecated",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "_evilUser", "type": "address"}],
        "name": "addBlackList",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "upgradedAddress",
        "outputs": [{"name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "", "type": "address"}],
        "name": "balances",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "maximumFee",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "_totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "unpause",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_maker", "type": "address"}],
        "name": "getBlackListStatus",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "", "type": "address"}, {"name": "", "type": "address"}],
        "name": "allowed",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "paused",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "who", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "pause",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "getOwner",
        "outputs": [{"name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [{"name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "newBasisPoints", "type": "uint256"},
            {"name": "newMaxFee", "type": "uint256"},
        ],
        "name": "setParams",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "amount", "type": "uint256"}],
        "name": "issue",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "amount", "type": "uint256"}],
        "name": "redeem",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"name": "remaining", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "basisPointsRate",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "", "type": "address"}],
        "name": "isBlackListed",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "_clearedUser", "type": "address"}],
        "name": "removeBlackList",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "MAX_UINT",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "newOwner", "type": "address"}],
        "name": "transferOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "_blackListedUser", "type": "address"}],
        "name": "destroyBlackFunds",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"name": "_initialSupply", "type": "uint256"},
            {"name": "_name", "type": "string"},
            {"name": "_symbol", "type": "string"},
            {"name": "_decimals", "type": "uint256"},
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": False, "name": "amount", "type": "uint256"}],
        "name": "Issue",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": False, "name": "amount", "type": "uint256"}],
        "name": "Redeem",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": False, "name": "newAddress", "type": "address"}],
        "name": "Deprecate",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "feeBasisPoints", "type": "uint256"},
            {"indexed": False, "name": "maxFee", "type": "uint256"},
        ],
        "name": "Params",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "_blackListedUser", "type": "address"},
            {"indexed": False, "name": "_balance", "type": "uint256"},
        ],
        "name": "DestroyedBlackFunds",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": False, "name": "_user", "type": "address"}],
        "name": "AddedBlackList",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": False, "name": "_user", "type": "address"}],
        "name": "RemovedBlackList",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "owner", "type": "address"},
            {"indexed": True, "name": "spender", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"},
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    {"anonymous": False, "inputs": [], "name": "Pause", "type": "event"},
    {"anonymous": False, "inputs": [], "name": "Unpause", "type": "event"},
]


from hexbytes import HexBytes

# This will be set automatically
private_key: str = None  # type: ignore


def initialize(_private_key: HexBytes) -> None:
    global private_key

    private_key = _private_key.hex().removeprefix("0x")
