import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models import engine, Article, User, UserArticles
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone


# api key 353b18c04a434382a6735f887b917e35
# arya ba8f03f6905c4da09053621aef023d3f
def fetch_articles(countries, categories):
    load_dotenv()  # reads .env and loads its variables into the environment

    newsapi = NewsApiClient(os.getenv("NEWSAPI_KEY"))

    # print(type(categories_string))
    # print(type(countries_string))
    # countries = countries_string.split(",")
    # categories = countries_string.split(",")
    for current_country in countries:
        for current_category in categories:
            print(f"DEBUG: country={current_country}, category={current_category}")
            top_headlines_response = newsapi.get_top_headlines(
                category=current_category,
                language='en',
                country=current_country
            )
            store_articles(top_headlines_response)


def store_articles(top_headlines_response):
    new_count = 0
    skipped_count = 0
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
                new_count += 1
            except IntegrityError:
                session.rollback()
                skipped_count += 1
                print(f"Skipped duplicate: {article['title']}")
        print(f"DEBUG: {new_count} new articles inserted, {skipped_count} duplicates skipped")
    with Session(engine) as session:
        count = session.scalar(select(func.count()).select_from(Article))
        print(f"Total articles inserted in db: {count}")

    with Session(engine) as session:
        total = session.scalar(select(func.count()).select_from(Article))
        most_recent = session.scalars(select(Article).order_by(Article.published_date.desc())).first()
        print(f"Total articles in table: {total}")
        print(f"Most recent published_date: {most_recent.published_date}")

def get_recent_articles_from_db():
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
    with Session(engine) as session:
        articles = session.scalars(
            select(Article).where(Article.published_date >= cutoff)
        ).all()
        return articles

def get_recent_unsent_articles(user_id):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)

    already_sent_subquery = (
        select(UserArticles.article_id)
        .where(UserArticles.user_id == user_id)
    )

    with Session(engine) as session:
        articles = session.scalars(
            select(Article)
            .where(Article.published_date >= cutoff)
            .where(Article.article_id.not_in(already_sent_subquery))
        ).all()
        return articles

def get_saved_preferences():
    with Session(engine) as session:
        user = session.scalars(select(User)).first()

        if user is None or not user.selected_countries:
            return None, None

        countries = user.selected_countries.split(",")
        categories = user.selected_categories.split(",")

        return countries, categories, user


if __name__ == "__main__":
    print("main function is here!")
    
