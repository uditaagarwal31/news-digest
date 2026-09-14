import os
import httpx
from dotenv import load_dotenv

load_dotenv()

topic = os.getenv("NTFY_TOPIC")
httpx.post(f"https://ntfy.sh/{topic}", data="Test message from Python!")