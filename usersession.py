from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models import engine, Article
from datetime import datetime
from fetch_news import top_headlines_response

# with Session(engine) as session:
#     new_article = Article(
#         title="test title",
#         url="test url",
#         source="udita brain",
#         published_date=datetime.datetime.now(),
#         content="test content",
#         summary="test summary",
#     )
#     session.add(new_article)
#     session.commit()
#     session.query(Article).all()


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

    session.commit()

    


with Session(engine) as session:
    count = session.scalar(select(func.count()).select_from(Article))
    print(f"Total articles: {count}")

# print(top_headlines_response["articles"][0]["title"])
# print(top_headlines_response["articles"][0]["url"])
# print(top_headlines_response["articles"][0]["source"]["name"])
# print(top_headlines_response["articles"][0]["publishedAt"])
# print(top_headlines_response["articles"][0]["content"])

  