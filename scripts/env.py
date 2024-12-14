import os

from dotenv import load_dotenv

load_dotenv()

RUSSIAN_LETTERS_LOWER = "юпхыяеаоиуйэцкьъзшщдлвмстрнгжчб"
RUSSIAN_LETTERS_UPPER = "ЮПХЫЯЕАОИУЙЭЦКЬЪЗШЩДЛВМСТРНГЖЧБ"
RUSSIAN_LETTERS = RUSSIAN_LETTERS_LOWER + RUSSIAN_LETTERS_UPPER

MEDIA_ROOT = os.getenv("MEDIA_ROOT")
DB_PATH = os.getenv("DB_PATH")
