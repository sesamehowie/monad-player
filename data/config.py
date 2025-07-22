import os
from dotenv import load_dotenv

load_dotenv()

MIN_PLAYERS = 1
MAX_PLAYERS = 2
CONTRACT_OWNER_PKEY = os.environ.get("CONTRACT_OWNER_PKEY")
LOTTERY_CA = os.environ.get("LOTTERY_CA")
MONAD_RPC_URL = os.environ.get("MONAD_RPC_URL")
AMOUNT_RANGE = [0.05, 0.2]
RAND_SLEEP_RANGE = [2, 7]
MIN_REQUIRED_BALANCE = 0.062
SLEEP_BETWEEN_ROUNDS = [1, 160]
