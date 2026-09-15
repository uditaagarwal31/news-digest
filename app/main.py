# app/main.py — becomes the FastAPI web app
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models import engine, User
from app.countries import COUNTRIES
from app.run_digest import run_digest_for_user, run_digest
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: runs once when the app starts
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_digest, "cron", hour=17, minute=20)
    scheduler.start()

    yield  # the app runs here, handling requests, until shutdown

    # Shutdown: runs once when the app stops
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
def show_form():
    country_checkboxes = ""
    for code, name in sorted(COUNTRIES.items(), key=lambda item: item[1]):
        country_checkboxes += f'<label class="country-option"><input type="checkbox" name="countries" value="{code}"> {name}</label>\n'

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
                border-radius: 14px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.06);
                padding: 32px;
                max-width: 460px;
                width: 100%;
            }}
            h2 {{
                margin-top: 0;
                margin-bottom: 4px;
                color: #1a1a1a;
                font-size: 22px;
            }}
            .subtitle {{
                color: #888;
                font-size: 14px;
                margin-bottom: 8px;
            }}
            .section-label {{
                font-weight: 600;
                margin-top: 28px;
                margin-bottom: 10px;
                color: #333;
                font-size: 14px;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .hint {{
                font-weight: 400;
                color: #999;
                font-size: 12px;
            }}
            .field-group {{
                margin-top: 20px;
            }}
            .field-group label {{
                display: block;
                font-weight: 600;
                font-size: 14px;
                color: #333;
                margin-bottom: 6px;
            }}
            .field-group input[type="text"] {{
                width: 100%;
                box-sizing: border-box;
                padding: 10px 12px;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                font-size: 14px;
                color: #1a1a1a;
                transition: border-color 0.15s, box-shadow 0.15s;
            }}
            .field-group input[type="text"]:focus {{
                outline: none;
                border-color: #2563eb;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }}
            .field-hint {{
                font-size: 12px;
                color: #999;
                margin-top: 4px;
            }}
            .country-list {{
                max-height: 200px;
                overflow-y: auto;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                padding: 6px 14px;
                background: #fafafa;
            }}
            .country-option {{
                display: block;
                padding: 7px 0;
                cursor: pointer;
                font-size: 14px;
                color: #333;
            }}
            .country-option:hover {{
                color: #2563eb;
            }}
            input[type="checkbox"] {{
                margin-right: 10px;
                transform: scale(1.1);
                accent-color: #2563eb;
            }}
            .category-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
            }}
            .category-pill {{
                display: flex;
                align-items: center;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 9px 12px;
                cursor: pointer;
                font-size: 14px;
                color: #333;
                transition: border-color 0.15s, background-color 0.15s;
            }}
            .category-pill:has(input:checked) {{
                border-color: #2563eb;
                background-color: #eff6ff;
                color: #1d4ed8;
                font-weight: 500;
            }}
            button {{
                margin-top: 28px;
                width: 100%;
                padding: 13px;
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: background-color 0.15s;
            }}
            button:hover {{
                background-color: #1d4ed8;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📰 News Digest</h2>
            <div class="subtitle">Sign up or update your preferences</div>
            <form action="/preferences" method="post">
                <div class="field-group">
                    <label for="user_name">Your name</label>
                    <input type="text" id="user_name" name="user_name" placeholder="Your username" required>
                </div>

                <div class="field-group">
                    <label for="ntfy_topic">ntfy topic</label>
                    <input type="text" id="ntfy_topic" name="ntfy_topic" placeholder="your-unique-topic-name" required>
                    <div class="field-hint">This is your private channel in the ntfy app — pick something only you know.</div>
                </div>

                <div class="section-label">🌍 Countries <span class="hint">(up to 3)</span></div>
                <div class="country-list">
                    {country_checkboxes}
                </div>

                <div class="section-label">🏷️ Categories <span class="hint">(up to 3)</span></div>
                <div class="category-grid">
                    <label class="category-pill"><input type="checkbox" name="categories" value="business"> Business</label>
                    <label class="category-pill"><input type="checkbox" name="categories" value="entertainment"> Entertainment</label>
                    <label class="category-pill"><input type="checkbox" name="categories" value="general"> General</label>
                    <label class="category-pill"><input type="checkbox" name="categories" value="health"> Health</label>
                    <label class="category-pill"><input type="checkbox" name="categories" value="science"> Science</label>
                    <label class="category-pill"><input type="checkbox" name="categories" value="sports"> Sports</label>
                    <label class="category-pill"><input type="checkbox" name="categories" value="technology"> Technology</label>
                </div>

                <button type="submit">Save preferences</button>
            </form>
        </div>
    </body>
    </html>
    """


@app.post("/preferences", response_class=HTMLResponse)
def save_preferences(
    ntfy_topic: str = Form(...),
    user_name: str = Form(...),
    countries: list[str] = Form(...),
    categories: list[str] = Form(...),
):
    with Session(engine) as session:
        #user = session.query(User).first()
        user = session.query(User).filter(User.ntfy_topic == ntfy_topic).first()
        countries_str = ",".join(countries[:3])
        categories_str = ",".join(categories[:3])

        if user is None:
            user = User(
                user_name=user_name,
                ntfy_topic=ntfy_topic,
                selected_countries=countries_str,
                selected_categories=categories_str,
            )
            session.add(user)
        else:
            user.selected_countries = countries_str
            user.selected_categories = categories_str
            user.ntfy_topic = ntfy_topic

        session.commit()
        session.refresh(user)  # ensures user.user_id is populated for a brand-new row

    run_digest_for_user(user)

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
                min-height: 100vh;      
                align-items: flex-start;   
            }}
            .card {{
                background: white;
                border-radius: 14px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.06);
                padding: 32px;
                max-width: 460px;
                width: 100%;
                height: auto;             
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
