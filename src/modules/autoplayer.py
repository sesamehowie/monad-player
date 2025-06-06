import random
from loguru import logger
from src.models.player import Player
from src.utils.helpers import rand_sleep, round_sleep
from data.config import (
    MAX_PLAYERS,
    MIN_PLAYERS,
    MIN_REQUIRED_BALANCE,
)


class AutoPlayer:
    def __init__(self, private_keys: list[str]):
        self.private_keys = private_keys
        self._players = self._get_all_players()
        self._eligible_players = self._get_eligible_players()

    def _get_all_players(self) -> list[Player]:
        return [
            Player(f"Player {num}", key)
            for num, key in enumerate(self.private_keys, start=1)
        ]

    def _get_eligible_players(self) -> list[Player]:
        logger.info("Getting eligible players")
        player_count = len(self._players)
        elig_players = []

        for player in self._players:
            balance = player.get_balance()
            if balance < int(MIN_REQUIRED_BALANCE * 10**18):
                continue
            else:
                elig_players.append(player)

        eligible_player_count = len(elig_players)

        if eligible_player_count == player_count:
            logger.info("All players are eligible")
        else:
            logger.info(f"Eligible player count: {len(elig_players)}/{player_count}")

        return elig_players

    def _claim_if_winner(self, prev_data: tuple):
        winner_address = prev_data[6]
        logger.info(f"Winner of the previous round: {winner_address}")
        for player in self._players:
            if player.address.lower() == winner_address.lower():
                player.claim_winnings()
        return False

    def _play_round(self):
        waiting_round_states = {0, 1, 2}
        player_count = random.randint(MIN_PLAYERS, MAX_PLAYERS)
        prev_data = self._players[0].check_prev()

        self._claim_if_winner(prev_data)

        if len(self._eligible_players) >= MAX_PLAYERS:
            random_players = random.sample(self._eligible_players, player_count)
        elif MIN_PLAYERS < len(self._eligible_players) < MAX_PLAYERS:
            random_players = random.sample(MIN_PLAYERS, len(self._eligible_players) - 1)
        else:
            random.shuffle(self._eligible_players)
            random_players = self._eligible_players

        round_state = int(self._eligible_players[0].check_round_state())
        bet_order = 1
        for player in random_players:
            if round_state in waiting_round_states:
                player.bet(wide_range=True if bet_order % 2 == 0 else False)
                rand_sleep()
                bet_order += 1
            else:
                break

        state = round_state

        while state != 3:
            state = int(self._eligible_players[0].check_round_state())
            if state == 0 or state == 1:
                break
            logger.info("Round not completed yet")
            rand_sleep()

        logger.success("Round completed.")
        return True

    def play_indefinitely(self) -> None:
        logger.info("Starting play process")

        rounds_played = 1
        while True:
            try:
                logger.info(f"Round {rounds_played} - Starting")
                if rounds_played > 1:
                    self._eligible_players = self._get_eligible_players()

                    if not self._eligible_players or len(self._eligible_players) < 2:
                        logger.debug(
                            "Not enough eligible players to play anymore. Stopping"
                        )
                        return

                self._play_round()
                logger.success(f"Round {rounds_played} - Successfully completed!")
            except Exception as e:
                logger.warning(f"Failed to complete round {rounds_played}: {str(e)}")
            finally:
                rounds_played += 1
                round_sleep()
