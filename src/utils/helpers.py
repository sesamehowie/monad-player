import time
import random
from data.config import RAND_SLEEP_RANGE, SLEEP_BETWEEN_ROUNDS
from loguru import logger


def rand_sleep() -> None:
    rand_t = random.randint(*RAND_SLEEP_RANGE)
    logger.debug(f"Sleeping for {rand_t} seconds...")
    time.sleep(rand_t)


def round_sleep() -> None:
    rand_t = random.randint(*SLEEP_BETWEEN_ROUNDS)
    logger.debug(f"Sleeping for {rand_t} seconds...")
    time.sleep(rand_t)
