# 📰 News Digest

A multi-user, personalized news digest app. Users sign up through a web form, pick which countries and categories they care about, and receive an AI-summarized digest pushed straight to their phone — both instantly on signup and automatically every morning.

Built end-to-end: FastAPI backend, SQLAlchemy/SQLite persistence, an external news API integration, custom deduplication and ranking logic, LLM-powered summarization via the Claude API, push notification delivery, and scheduled background jobs.

## Why I built this

I wanted a project that would force me to work across a full stack outside my day-to-day work — a real Python backend, a real database, real third-party API integrations, and real production-style problems (duplicate data, rate limits, timezones, multi-tenancy) rather than a tutorial-shaped toy app.

## What it does

1. A user visits the signup page, enters their name, a private [ntfy](https://ntfy.sh) topic (their delivery channel), and selects up to 3 countries and 3 categories they're interested in.
2. On signup, the app immediately fetches fresh headlines matching their preferences, deduplicates near-identical stories from different sources, ranks them by source coverage and recency, summarizes the top 7 with Claude, and pushes a formatted digest to their phone.
3. Every morning, a scheduled background job repeats this automatically for every signed-up user — without re-sending anything they've already received.

## Architecture

```
Signup form (FastAPI) ──▶ User + preferences saved to SQLite
                                      │
                                      ▼
                        ┌─────────────────────────┐
                        │      Digest pipeline      │
                        │                          │
   NewsAPI  ──fetch──▶  │  Fetch → Dedup → Rank →  │ ──▶ Claude API (summarize)
                        │                          │
                        └─────────────────────────┘
                                      │
                                      ▼
                              ntfy.sh (push notification)
                                      │
                                      ▼
                         articles_sent_to_user (tracking)
```

**Scheduling:** an in-process APScheduler background job triggers the full pipeline for every user every morning, running inside the same FastAPI process that serves the signup form.

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Backend framework | FastAPI | Async-friendly, minimal boilerplate, good fit for a small API + form service |
| Database / ORM | SQLite + SQLAlchemy | Zero-setup persistence for a personal-scale project; ORM keeps schema and queries in Python |
| News source | [NewsAPI](https://newsapi.org) | Simple REST API with country/category filtering |
| Deduplication | [RapidFuzz](https://github.com/rapidfuzz/RapidFuzz) | Fuzzy string matching to group near-identical headlines from different outlets |
| Summarization | Claude API (Haiku) | Fast, cost-effective batched summarization of ranked articles |
| Delivery | [ntfy.sh](https://ntfy.sh) | Simple, auth-free push notifications — no carrier compliance overhead |
| Scheduling | APScheduler | In-process cron-style scheduling, no external infrastructure needed |

## Key engineering decisions worth highlighting

- **Deduplication logic**: articles are grouped by fuzzy title similarity (comparing each new article against *every* existing member of a candidate group, not just the first, to avoid topic drift within a group), then ranked by a combination of source coverage and recency, with top-K selection via a heap-style pattern.
- **Multi-user design without full authentication**: each user's ntfy topic doubles as their account identifier — a deliberate scope decision to avoid building password auth for a project at this stage, while still supporting genuinely independent multi-user accounts.
- **Per-user delivery tracking**: a dedicated `articles_sent_to_user` table ensures no user ever receives the same story twice, even across overlapping recency windows.
- **Batched LLM summarization**: all top-ranked articles for a user are summarized in a single Claude API call (with defensive JSON parsing, since models sometimes wrap structured output in markdown fences) rather than one call per article — reducing cost and latency.
- **Resilient data handling**: unique constraints prevent duplicate article storage on re-fetch; timezone-aware datetime comparisons avoid subtle bugs when filtering by recency.

## Project structure

```
app/
├── main.py              # FastAPI app: signup form, preferences route, scheduler startup
├── models.py             # SQLAlchemy models: Article, User, UserArticles
├── countries.py           # NewsAPI country code → display name mapping
├── fetch_and_store.py      # NewsAPI integration + article persistence
├── rank.py                 # Deduplication (fuzzy matching) and ranking logic
├── summary.py               # Batched Claude API summarization
├── notification.py           # ntfy.sh push notification delivery
└── run_digest.py               # Pipeline orchestration, per-user and scheduled
```

## Running it locally

### Prerequisites
- Python 3.11+
- API keys for: [NewsAPI](https://newsapi.org) (free tier), [Anthropic](https://console.anthropic.com) (Claude API)
- The [ntfy app](https://ntfy.sh) installed on your phone (no account needed)

### Setup

```bash
# Clone and enter the project
git clone <repo-url>
cd news-digest-project

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```
NEWSAPI_KEY=your_newsapi_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Initialize the database

```bash
python -m app.models
```

### Run the app

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` to sign up. Enter a unique ntfy topic name, subscribe to that same topic in the ntfy app on your phone, and select your preferences — you'll receive your first digest within moments of signing up, and automatically every morning after that.

## What I'd build next

- Deploy to a persistent host (Render/Railway) so the scheduler runs 24/7, not just while my laptop is on
- Move to a production-tier news API, since NewsAPI's free tier is explicitly development-only
- Add Alembic migrations instead of drop-and-recreate schema changes
- Share fetch calls across users with overlapping preferences to reduce API usage
- Move the signup-triggered digest to a background task, so the confirmation page returns instantly instead of waiting on the full pipeline

---

*Built by Udita Agarwal as a self-directed project to build hands-on experience with Python, FastAPI, and LLM-integrated backend systems.*
