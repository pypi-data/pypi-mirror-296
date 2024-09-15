from enum import IntEnum

from .client import client
from . import config


class ChainId(IntEnum):
    ETHEREUM = 1
    OP = 10
    POLYGON = 137
    OPBNB = 204
    MANTLE = 5000
    BASE = 8453
    MODE = 34443
    ARBITRUM = 42161
    CELO = 42220
    AVALANCHE_C_CHAIN = 43314
    BLAST = 81457
    SCROLL = 54352

    @staticmethod
    def from_name(name: str):
        return CHAIN_IDS[name]

    def __str__(self):
        return CHAIN_NAMES[self]


CHAIN_NAMES = {
    ChainId.ETHEREUM: "ethereum",
    ChainId.OP: "optimism",
    ChainId.POLYGON: "polygon",
    ChainId.OPBNB: "opbnb",
    ChainId.MANTLE: "mantle",
    ChainId.BASE: "base",
    ChainId.MODE: "mode",
    ChainId.ARBITRUM: "arbitrum",
    ChainId.CELO: "celo",
    ChainId.AVALANCHE_C_CHAIN: "avalanche",
    ChainId.BLAST: "blast",
    ChainId.SCROLL: "scroll",
}

CHAIN_IDS = {name: id for id, name in CHAIN_NAMES.items()}


class Token:
    __slots__ = ("chain", "symbol", "chain_id", "contract_address", "decimals")

    def __init__(self, identifier: str):
        chain_name, self.symbol = identifier.split("-")
        self.chain = Chain(ChainId.from_name(chain_name))
        asset_data = self.chain.data["assets"][self.symbol]
        self.contract_address: str = asset_data["address"]
        self.decimals: int = asset_data["decimals"]

    @classmethod
    def from_components(cls, chain: ChainId, symbol: str):
        return cls(f"{chain.name}-{symbol}")

    def __eq__(self, other) -> bool:
        return self.chain == other.chain and self.symbol == other.symbol

    def __repr__(self) -> str:
        return f"{self.chain}-{self.symbol}"


class Chain:
    __slots__ = ("name", "id", "data", "lz_cid", "rpc_url")

    def __init__(self, id: ChainId):
        self.id = id
        self.data = client.deployments[self.id]
        self.lz_cid: int = self.data["lz_cid"]  # type: ignore
        self.rpc_url = config.rpc_urls[self.id]

    @property
    def name(self) -> str:
        return str(self.id)

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __repr__(self) -> str:
        return self.name
