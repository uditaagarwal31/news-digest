# app/main.py — becomes the FastAPI web app
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models import engine, User

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def show_form():
    return """
    <html>
    <body>
        <h2>News Digest Preferences</h2>
        <form action="/preferences" method="post">
            <p>Countries (pick up to 3):</p>
            <input type="checkbox" name="countries" value="us"> US<br>
            <input type="checkbox" name="countries" value="india"> India<br>
            <input type="checkbox" name="countries" value="world"> World<br>

            <p>Categories (pick up to 3):</p>
            <input type="checkbox" name="categories" value="business"> Business<br>
            <input type="checkbox" name="categories" value="entertainment"> Entertainment<br>
            <input type="checkbox" name="categories" value="general"> General<br>
            <input type="checkbox" name="categories" value="health"> Health<br>
            <input type="checkbox" name="categories" value="science"> Science<br>
            <input type="checkbox" name="categories" value="sports"> Sports<br>
            <input type="checkbox" name="categories" value="technology"> Technology<br>

            <button type="submit">Save Preferences</button>
        </form>
    </body>
    </html>
    """

@app.post("/preferences")
def save_preferences(
    countries: list[str] = Form(...),
    categories: list[str] = Form(...),
):
    with Session(engine) as session:
        user = session.query(User).first()

        countries_str = ",".join(countries[:3])
        categories_str = ",".join(categories[:3])

        if user is None:
            user = User(
                user_name="Udita",
                user_number="local-user",
                selected_countries=countries_str,
                selected_categories=categories_str,
            )
            session.add(user)
        else:
            user.selected_countries = countries_str
            user.selected_categories = categories_str

        session.commit()

    return {"message": "Preferences saved!", "countries": countries_str, "categories": categories_str}


# from app.fetch_and_store import fetch_articles, store_articles, get_all_articles_from_db
# from app.rank import dedup_articles, rank_and_limit
# from app.summary import summarise_article

# countries = ['us', 'in', 'cn', 'ca']
# categories = ['business', 'entertainment']

# fetch_articles(countries, categories)

# articles_from_db = get_all_articles_from_db()

# total_groups = dedup_articles(articles_from_db)


# top_results = rank_and_limit(total_groups, limit=7)


# summarise_article(top_results)