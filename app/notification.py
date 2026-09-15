import os
import httpx
from dotenv import load_dotenv

def send_notification(article_titles, summaries):
    load_dotenv()

    message_being_sent = ""

    for i, (title, summary) in enumerate(zip(article_titles, summaries), start=1):
        message_being_sent += f"{i}. 📰 {title}\n{summary}\n\n"

    topic = os.getenv("NTFY_TOPIC")
    headers = {
        "Title": "Your Morning News Digest",
        "Tags": "newspaper",
    }
    httpx.post(f"https://ntfy.sh/{topic}", data=message_being_sent.strip(), headers=headers)

