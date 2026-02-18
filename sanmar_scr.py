import pandas as pd
import requests
from gspread_dataframe import set_with_dataframe
from urllib.parse import quote
from datetime import datetime, timedelta
import pytz
import gspread
import os

client_id = os.environ['ZOHO_CLIENT_ID']
client_secret = os.environ['ZOHO_CLIENT_SECRET']

# Current time and 24 hours ago
ist = pytz.timezone('Asia/Kolkata')
today_date = datetime.now(ist).strftime('%Y-%m-%d')

TIME_IN  = f"{today_date}T00:00:00+05:30"
TIME_OUT = f"{today_date}T23:59:59+05:30"

criteria = f"(Created_Time:between:{TIME_IN},{TIME_OUT})"
params = {"criteria": criteria}


#####################################################
## GENERATE AUTH AND REFRESH CODE

# # Generate Fresh Token
# auth_code = os.environ['ZOHO_AUTH_CODE']
# redirect_uri = "https://your-registered-redirect-url.com"

# post_url = "https://accounts.zoho.in/oauth/v2/token"

# # Use these exact key names
# token_data = {
#     "grant_type": "authorization_code",
#     "client_id": client_id,
#     "client_secret": client_secret,
#     "redirect_uri": redirect_uri,
#     "code": auth_code
# }

# token_response = requests.post(post_url, data=token_data)

#####################################################

access_token =  os.environ['ZOHO_ACCESS_TOKEN']
refresh_token =  os.environ['ZOHO_REFRESH_TOKEN']
scope = 'ZohoCRM.modules.Leads.READ ZohoCRM.modules.Events.READ ZohoCRM.modules.Deals.READ'

# Get a Refresh Token
refresh_url = "https://accounts.zoho.in/oauth/v2/token"

data = {'refresh_token': refresh_token,
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'refresh_token'}

response = requests.post(refresh_url, data=data)
new_tokens = response.json()
access_token = new_tokens.get('access_token')

#####################################################

# FETCH ZOHO LEADS DATA

get_url_leads = "https://www.zohoapis.in/crm/v8/Leads/search"
headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
get_response = requests.get(get_url_leads, headers=headers, params=params)

try:
    raw_records = get_response.json().get('data', [])
    df_leads_zoho = pd.json_normalize(raw_records)
    # df_leads_zoho['Created_Time'] = pd.to_datetime(df_leads_zoho['Created_Time'], utc=True).dt.tz_convert('Asia/Kolkata')
except:
    df_leads_zoho = pd.DataFrame()

#####################################################

#FETCH ZOHO DEALS DATA

get_url_deals = "https://www.zohoapis.in/crm/v8/Deals/search"
headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
get_response = requests.get(get_url_deals, headers=headers, params=params)

try:
    raw_records = get_response.json().get('data', [])
    df_deals_zoho = pd.json_normalize(raw_records)
    # df_deals_zoho['Created_Time'] = pd.to_datetime(df_deals_zoho['Created_Time'],  utc=True).dt.tz_convert('Asia/Kolkata')
except:
    df_deals_zoho = pd.DataFrame()

#####################################################

#SETUP GOOGLE SHEETS

# 1. Authenticate using User Credentials (Client ID & Secret)
gc = gspread.oauth(
    credentials_filename=os.environ['CLIENT_SECRETS_JSON'],
    authorized_user_filename=os.environ['AUTH_USER_JSON']
)


sh             = gc.open_by_url(os.environ['GOOGLE_SHEET_URL'])
sheet_leads    = sh.worksheet("Leads")
sheet_deals    = sh.worksheet("Deals")

#####################################################

#UPDATE GOOGLE SHEET

def update_sheet(worksheet, df_new):
    if df_new.empty:
        print("No new data, skipping.")
        return
    print(f"Zoho columns: {df_new.columns.tolist()}")

    try:
        id_col       = worksheet.find('id').col
        existing_ids = worksheet.col_values(id_col)
        print(f"Found id column at position: {id_col}")
        print(f"Total existing IDs in sheet: {len(existing_ids)}")
    except:
        print("Could not find 'id' column in sheet header")
        return

    df_new = df_new.astype(str)

    for _, row in df_new.iterrows():
        row_id = str(row['id'])
        if row_id in existing_ids:
            row_number = existing_ids.index(row_id) + 1
            print(f"Updating existing row {row_number} for id {row_id}")
            worksheet.update(f'A{row_number}', [row.tolist()])
        else:
            print(f"Appending new id {row_id}")
            worksheet.append_row(row.tolist(), value_input_option='USER_ENTERED')


update_sheet(sheet_leads, df_leads_zoho)
update_sheet(sheet_deals, df_deals_zoho)

#Sort sheet by Created_Time after all updates
def sort_sheet_by_date(worksheet):
    df = pd.DataFrame(worksheet.get_all_records())
    if df.empty:
        return
    df = df.sort_values('Created_Time', ascending=True)
    set_with_dataframe(worksheet, df, row=1, col=1, include_index=False, include_column_header=True)

sort_sheet_by_date(sheet_leads)
sort_sheet_by_date(sheet_deals)
