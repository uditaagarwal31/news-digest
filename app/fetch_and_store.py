import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models import engine, Article
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# api key 353b18c04a434382a6735f887b917e35
# arya ba8f03f6905c4da09053621aef023d3f
def fetch_articles(countries, categories):
    load_dotenv()  # reads .env and loads its variables into the environment

    newsapi = NewsApiClient(os.getenv("NEWSAPI_KEY"))

    for current_country in countries:
        for current_category in categories:
            top_headlines_response = newsapi.get_top_headlines(
                category=current_category,
                language='en',
                country=current_country
            )
            store_articles(top_headlines_response)


def store_articles(top_headlines_response):
    with Session(engine) as session:
        for article in top_headlines_response["articles"]:
            new_article = Article(
                title=article["title"],
                url=article["url"],
                source=article["source"]["name"],
                published_date=datetime.fromisoformat(article["publishedAt"]),
                content=article["content"]
            )
            session.add(new_article)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                print(f"Skipped duplicate: {article['title']}")

    with Session(engine) as session:
        count = session.scalar(select(func.count()).select_from(Article))
        print(f"Total articles inserted in db: {count}")


def get_all_articles_from_db():
    with Session(engine) as session:
        statement = select(Article)
        all_articles = session.scalars(statement).all()
        print("Total articles returned from db", len(all_articles))
    return all_articles


if __name__ == "__main__":
    print("main function is here!")
    
