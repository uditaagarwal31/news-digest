from app.fetch_and_store import fetch_articles, store_articles, get_all_articles_from_db
from app.rank import dedup_articles

countries = ['us', 'in', 'cn', 'ca']
categories = ['business', 'entertainment']

fetch_articles(countries, categories)

articles_from_db = get_all_articles_from_db()

dedup_articles(articles_from_db)
