# app/run_digest.py — your existing pipeline code moves here, unchanged
from app.fetch_and_store import fetch_articles, store_articles, get_all_articles_from_db, get_saved_preferences
from app.rank import dedup_articles, rank_and_limit
from app.summary import summarise_article

def run_digest():
   # countries = ['us', 'in', 'cn', 'ca']
   # categories = ['business', 'entertainment']

    countries, categories = get_saved_preferences()

    if not countries or not categories:
        print("No preferences saved yet — visit the form to set them.")
        return

    fetch_articles(countries, categories)
    articles_from_db = get_all_articles_from_db()
    total_groups = dedup_articles(articles_from_db)
    top_results = rank_and_limit(total_groups, limit=7)
    summarise_article(top_results)

if __name__ == "__main__":
    run_digest()