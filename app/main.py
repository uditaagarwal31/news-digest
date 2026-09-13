from app.fetch_and_store import fetch_articles, store_articles, get_all_articles_from_db
from app.rank import dedup_articles, rank_and_limit

countries = ['us', 'in', 'cn', 'ca']
categories = ['business', 'entertainment']

fetch_articles(countries, categories)

articles_from_db = get_all_articles_from_db()

total_groups = dedup_articles(articles_from_db)


top_results = rank_and_limit(total_groups, limit=7)

for result in top_results:
    print(result.title)
