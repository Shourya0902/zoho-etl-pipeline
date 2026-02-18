# Zoho ETL Pipeline

An automated data sync pipeline that fetches daily CRM data from Zoho and syncs it to Google Sheets using GitLab CI/CD.

## What It Does
- Fetches Leads and Deals created **today** from Zoho CRM API
- Upserts data into Google Sheets — updates existing records by ID, appends new ones
- Sorts the sheet by `Created_Time` after every update
- Runs automatically every day via GitLab CI/CD

## Tech Stack
- Python
- Zoho CRM API (OAuth 2.0)
- Google Sheets API (gspread)
- GitLab CI/CD
- Pandas

## Project Structure
zoho-etl-pipeline/
├── sanmar_scr.py        # Main pipeline script
├── requirements.txt     # Python dependencies
├── .gitlab-ci.yml       # GitLab CI/CD configuration
├── .env.example         # Environment variables template
└── .gitignore

## Setup

### 1. Clone the repository
git clone https://github.com/your-username/zoho-etl-pipeline.git
cd zoho-etl-pipeline

### 2. Install dependencies
pip install -r requirements.txt

### 3. Set environment variables
Copy `.env.example` and fill in your credentials:
ZOHO_CLIENT_ID=
ZOHO_CLIENT_SECRET=
ZOHO_REFRESH_TOKEN=
ZOHO_ACCESS_TOKEN=
CLIENT_SECRETS_JSON=
AUTH_USER_JSON=
GOOGLE_SHEET_URL=

### 4. Zoho Setup
- Create a Zoho API client at [Zoho API Console](https://api-console.zoho.in)
- Generate a refresh token with the required scopes:
  - `ZohoCRM.modules.Leads.READ`
  - `ZohoCRM.modules.Deals.READ`

### 5. Google Sheets Setup
- Enable Google Sheets API in Google Cloud Console
- Create OAuth 2.0 credentials and download `client_secrets.json`
- Share your Google Sheet with the OAuth account

## GitLab CI/CD
All environment variables are stored securely in GitLab under:
**Settings → CI/CD → Variables**

The pipeline runs on a scheduled trigger and requires no manual intervention.

## Author
Shourya Marwaha
