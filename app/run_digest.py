# app/run_digest.py — your existing pipeline code moves here, unchanged
from app.fetch_and_store import fetch_articles, store_articles, get_recent_articles_from_db, get_saved_preferences
from app.rank import dedup_articles, rank_and_limit
from app.summary import summarise_article
from app.notification import send_notification

def run_digest():
   # countries = ['us', 'in', 'cn', 'ca']
   # categories = ['business', 'entertainment']

    countries, categories = get_saved_preferences()

    if not countries or not categories:
        print("No preferences saved yet — visit the form to set them.")
        return


    fetch_articles(countries, categories)
    articles_from_db = get_recent_articles_from_db()
    print(f"DEBUG: {len(articles_from_db)} articles after date filter")

    total_groups = dedup_articles(articles_from_db)
    print(f"DEBUG: {len(total_groups)} groups after dedup")

    top_results = rank_and_limit(total_groups, limit=7)
    print(f"DEBUG: {len(top_results)} results after rank/limit")
    articles_titles_block, summaries = summarise_article(top_results)
    send_notification(articles_titles_block,summaries)

if __name__ == "__main__":
    run_digest()