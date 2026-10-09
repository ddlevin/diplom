import os
from dotenv import load_dotenv

load_dotenv()

# API
BASE_URL: str = "https://api.poiskkino.dev"
API_KEY: str = os.getenv("POISKKINO_API_KEY", "")
REQUEST_TIMEOUT: int = 10

# UI
DASHBOARD_URL: str = "https://dashboard.poiskkino.dev"
LOGIN_EMAIL: str = os.getenv("POISKKINO_LOGIN_EMAIL", "")
LOGIN_PASSWORD: str = os.getenv("POISKKINO_LOGIN_PASSWORD", "")
