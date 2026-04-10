# Zoho CRM ETL & Sales Analytics Pipeline

An automated data pipeline that extracts daily Leads and Deals data from Zoho CRM via REST API, transforms it using Python, and loads it into Google Sheets — with Looker dashboards on top for live sales reporting. Scheduled and executed daily via GitLab CI/CD.

---

## The Problem It Solves

Sales teams at most companies still rely on manual CRM exports to track pipeline health. That means stale data, inconsistent numbers across teams, and no single source of truth. This pipeline eliminates all of that — every morning the data is fresh, the sheet is updated, and the Looker dashboard reflects the current state of the pipeline without anyone lifting a finger.

---

## How It Works

```
Zoho CRM API → Python (Extract + Transform) → Google Sheets → Looker Dashboard
                          ↑
               GitLab CI/CD (runs daily on schedule)
```

1. GitLab CI/CD triggers the pipeline on a daily schedule
2. OAuth 2.0 token is refreshed automatically using stored credentials
3. Leads and Deals created in the last 24 hours are fetched from Zoho CRM v8 API
4. Data is normalised and cleaned using pandas
5. Google Sheets is updated — existing records are updated in place, new records are appended
6. Sheet is sorted by `Created_Time` after every run
7. Looker reads from Google Sheets and refreshes dashboards automatically

---

## Key Features

- **OAuth 2.0 token refresh** — no manual re-authentication needed
- **Upsert logic** — existing records updated, new ones appended, no duplicates
- **IST timezone handling** — daily window correctly scoped to Indian Standard Time
- **Env-based secrets** — all credentials stored as GitLab CI/CD environment variables, nothing hardcoded
- **Zero manual intervention** — fully hands-off once set up

---

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python |
| Data Processing | pandas |
| CRM Source | Zoho CRM v8 API |
| Auth | OAuth 2.0 (Zoho + Google) |
| Destination | Google Sheets (via gspread) |
| Visualisation | Looker |
| Automation | GitLab CI/CD (scheduled pipelines) |

---

## Dashboard Metrics

The Looker dashboard gives sales and ops teams visibility into:

- Daily leads created
- Daily deals created and their pipeline value
- Deal stage breakdown and funnel progression
- Sales performance by owner
- Filterable by date range and owner

---

## Project Structure

```
zoho-etl-pipeline/
├── sanmar_scr.py        # Main ETL script (extract, transform, load)
├── .gitlab-ci.yml       # CI/CD config — runs daily on schedule
├── .env.example         # Template for required environment variables
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Environment Variables Required

```
ZOHO_CLIENT_ID
ZOHO_CLIENT_SECRET
ZOHO_ACCESS_TOKEN
ZOHO_REFRESH_TOKEN
CLIENT_SECRETS_JSON       # Path to Google OAuth credentials
AUTH_USER_JSON            # Path to Google authorised user file
GOOGLE_SHEET_URL          # Target Google Sheet URL
```

All secrets are stored as GitLab CI/CD variables — never in the codebase.

---

## Running Locally

```bash
git clone https://github.com/Shourya0902/zoho-etl-pipeline.git
cd zoho-etl-pipeline
pip install -r requirements.txt

# Copy and fill in your credentials
cp .env.example .env

python sanmar_scr.py
```

---

## Future Improvements

- Migrate destination from Google Sheets to PostgreSQL or BigQuery for scale
- Add data validation and quality checks before loading
- Implement logging and alerting for pipeline failures
- Add conversion rate and deal velocity metrics to the dashboard

---

## Author

**Shourya Marwaha**
MSc Data Science & Analytics, University of Leeds | MBA (Finance) | BTech (Mechanical Engineering)

[LinkedIn](https://www.linkedin.com/in/shouryamarwaha/) · [shouryamarwaha@gmail.com](mailto:shouryamarwaha@gmail.com)
