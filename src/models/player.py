import random
from decimal import Decimal, getcontext
from ..client.eth_client import EthClient
from ..network.network import Monad
from ..interfaces.interfaces import MonRollInterface

getcontext().prec = 4


class Player(EthClient):
    def __init__(self, account_name, private_key, network=Monad):
        super().__init__(account_name, private_key, network)
        self.interface = MonRollInterface

    def bet(self, wide_range: bool = True):
        min_amount = Decimal("0.05")
        max_amount = Decimal("0.2")
        short_step = Decimal("0.01")
        wide_step = Decimal("0.05")

        short_bets = [
            min_amount + i * short_step
            for i in range(int((max_amount - min_amount) / short_step) + 1)
        ]
        wide_bets = [
            min_amount + i * wide_step
            for i in range(int((max_amount - min_amount) / wide_step) + 1)
        ]
        item_to_choose = wide_bets if wide_range else short_bets

        chosen_amount = random.choice(item_to_choose)
        return MonRollInterface.execute_write_function(
            "bet",
            self,
            [],
            int(chosen_amount * 10**18),
            False,
        )

    def claim_winnings(self):
        return MonRollInterface.execute_write_function(
            "claim", self, [self.address], 0, False
        )

    def check_round_state(self):
        return MonRollInterface.execute_read_function("roundState", self, [])

    def check_prev(self):
        return MonRollInterface.execute_read_function("prev", self, [])
