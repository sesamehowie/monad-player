from dataclasses import dataclass
from data.config import MONAD_RPC_URL


@dataclass
class Network:
    name: str
    chain_id: int
    native_token: str
    rpc_list: list[str]
    scanner: str


Monad = Network(
    "Monad Testnet",
    10143,
    "MON",
    [MONAD_RPC_URL],
    "https://testnet.monadexplorer.com",
)
