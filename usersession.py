from sqlalchemy.orm import Session
from models import engine, Article
import datetime
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
    new_article = Article(
        title="test title",
        url="test url",
        source="udita brain",
        published_date=datetime.datetime.now(),
        content="test content",
        summary="test summary",
    )
    session.add(new_article)
    session.commit()
    session.query(Article).all()