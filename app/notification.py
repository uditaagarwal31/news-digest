import os
import httpx
from dotenv import load_dotenv
from sqlalchemy import select, func
from app.models import engine, UserArticles
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone


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


def mark_articles_as_sent(user_id, article_ids):
    with Session(engine) as session:
        for curr_article_id in article_ids:
                article_sent = UserArticles(
                    article_id = curr_article_id,
                    user_id = user_id,
                    sent_date = datetime.now(timezone.utc)
                )
                session.add(article_sent)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()