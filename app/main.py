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
    <head>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background-color: #f4f6f8;
                display: flex;
                justify-content: center;
                padding: 40px 20px;
                margin: 0;
            }
            .card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                padding: 32px;
                max-width: 420px;
                width: 100%;
            }
            h2 {
                margin-top: 0;
                color: #1a1a1a;
            }
            .section-label {
                font-weight: 600;
                margin-top: 24px;
                margin-bottom: 8px;
                color: #444;
            }
            label {
                display: block;
                padding: 8px 0;
                cursor: pointer;
                font-size: 15px;
                color: #333;
            }
            input[type="checkbox"] {
                margin-right: 10px;
                transform: scale(1.1);
            }
            button {
                margin-top: 28px;
                width: 100%;
                padding: 12px;
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
            }
            button:hover {
                background-color: #1d4ed8;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📰 News Digest Preferences</h2>
            <form action="/preferences" method="post">
                <div class="section-label">Countries (pick up to 3)</div>
                <label><input type="checkbox" name="countries" value="us"> 🇺🇸 US</label>
                <label><input type="checkbox" name="countries" value="india"> 🇮🇳 India</label>
                <label><input type="checkbox" name="countries" value="world"> 🌍 World</label>

                <div class="section-label">Categories (pick up to 3)</div>
                <label><input type="checkbox" name="categories" value="business"> Business</label>
                <label><input type="checkbox" name="categories" value="entertainment"> Entertainment</label>
                <label><input type="checkbox" name="categories" value="general"> General</label>
                <label><input type="checkbox" name="categories" value="health"> Health</label>
                <label><input type="checkbox" name="categories" value="science"> Science</label>
                <label><input type="checkbox" name="categories" value="sports"> Sports</label>
                <label><input type="checkbox" name="categories" value="technology"> Technology</label>

                <button type="submit">Save Preferences</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/preferences", response_class=HTMLResponse)
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

    countries_display = ", ".join(countries[:3])
    categories_display = ", ".join(categories[:3])

    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background-color: #f4f6f8;
                display: flex;
                justify-content: center;
                padding: 40px 20px;
                margin: 0;
            }}
            .card {{
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                padding: 32px;
                max-width: 420px;
                width: 100%;
                text-align: center;
            }}
            .checkmark {{
                font-size: 48px;
                margin-bottom: 8px;
            }}
            h2 {{
                margin-top: 0;
                color: #1a1a1a;
            }}
            .pref-row {{
                text-align: left;
                margin-top: 20px;
                padding: 12px 16px;
                background: #f0f4f9;
                border-radius: 8px;
            }}
            .pref-label {{
                font-weight: 600;
                color: #555;
                font-size: 13px;
                text-transform: uppercase;
            }}
            .pref-value {{
                color: #222;
                font-size: 15px;
                margin-top: 4px;
            }}
            a {{
                display: inline-block;
                margin-top: 24px;
                color: #2563eb;
                text-decoration: none;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="checkmark">✅</div>
            <h2>Preferences Saved</h2>
            <div class="pref-row">
                <div class="pref-label">Countries</div>
                <div class="pref-value">{countries_display}</div>
            </div>
            <div class="pref-row">
                <div class="pref-label">Categories</div>
                <div class="pref-value">{categories_display}</div>
            </div>
            <a href="/">← Edit preferences</a>
        </div>
    </body>
    </html>
    """
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