from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime
from sqlalchemy import create_engine, Text, DateTime, UniqueConstraint

engine = create_engine("sqlite:///news.db", echo=True)

# declarative base class
class Base(DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = "article"
    __table_args__ = (UniqueConstraint("url"),)
    article_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(255))
    published_date: Mapped[datetime.date] = mapped_column(DateTime)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    #summary: Mapped[str] = mapped_column(Text)


class User(Base):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(255))
    user_number: Mapped[str] = mapped_column(String(255))
    selected_countries: Mapped[str] = mapped_column(String(255))
    selected_categories: Mapped[str] = mapped_column(String(255))


class UserArticles(Base):
    __tablename__ = "articles_sent_to_user"       
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("article.article_id"), primary_key=True)
    sent_date: Mapped[datetime.date] = mapped_column(DateTime)


Base.metadata.create_all(engine)
