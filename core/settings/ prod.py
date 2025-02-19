from .base import *

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('/env/.env.prod'))
