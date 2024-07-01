from os import environ
from pathlib import Path

TOKEN = environ.get("EBAY_KZ_BOT", "define me!")
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'
CALC_DB_FILE = BASE_DIR / 'calc.sqlite'
USERS_DB = BASE_DIR / 'users.sqlite'
DATA_DB = BASE_DIR / 'data.sqlite'