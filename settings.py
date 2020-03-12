# settings.py
from pathlib import Path  # python3 only
from dotenv import load_dotenv
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
HOST_URL = os.getenv('HOST_URL')
HOST_PORT = os.getenv('HOST_PORT')


