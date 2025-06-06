import time
import random
from web3 import Web3
from loguru import logger
from eth_account import Account
from ..network.network import Network
from web3.contract.contract import Contract


class EthClient:
    def __init__(self, account_name: str, private_key: str, network: Network):
        self.account_name = account_name
        self.private_key = private_key
        self.network = network
        self.rpc = (
            random.choice(self.network.rpc_list)
            if len(self.network.rpc_list) > 1
            else self.network.rpc_list[0]
        )
        self.account = Account.from_key(self.private_key)
        self.address = self.account.address
        self.w3 = Web3(Web3.HTTPProvider(self.rpc))

        logger.debug(
            f"Created eth client for wallet {self.address} on {network.name} network"
        )

    def get_balance(self):
        try:
            balance = self.w3.eth.get_balance(self.address)
            return balance
        except Exception as e:
            logger.warning(
                f"Failed to get balance for address {self.address}: {str(e)}"
            )
            logger.debug("Sleeping for 15 seconds before trying to get balance again")
            time.sleep(15)
            return self.get_balance()

    def get_nonce(self):
        return self.w3.eth.get_transaction_count(self.address)

    def get_contract(self, contract_addr: str, abi: str) -> Contract:
        return self.w3.eth.contract(address=contract_addr, abi=abi)

    def sign_and_send_tx(self, tx_dict: dict):
        signed = self.w3.eth.account.sign_transaction(
            transaction_dict=tx_dict, private_key=self.private_key
        )

        if signed:
            tx_hash = self.w3.eth.send_raw_transaction(
                transaction=signed.raw_transaction
            )

            if tx_hash:
                logger.success(
                    f"{self.account_name} | Transaction: {self.network.scanner}/tx/0x{tx_hash.hex()}"
                )

            return True if tx_hash else False

        return False
