

import pandas as pd
import requests
from gspread_dataframe import set_with_dataframe
from urllib.parse import quote
from datetime import datetime, timedelta
import pytz
import gspread

client_id = '1000.500COYWHDJTT61DFM00ZZB9XHCQT2M'
client_secret = 'a60b2ee703b497635327e97999cd563f2c2d436a0e'

# Current time and 24 hours ago
today_date = datetime.now().strftime('%Y-%m-%d')

# Manually add the Zoho-required timestamps
TIME_IN = f"{today_date}T00:00:00+05:30"
TIME_OUT = f"{today_date}T23:59:59+05:30"

# # Manually add the Zoho-required timestamps
# TIME_IN = f"2025-11-01T00:00:00+05:30"
# TIME_OUT = f"2026-02-17T23:59:59+05:30"


criteria = "(Created_Time:between:" + TIME_IN + "," + TIME_OUT + ")"
params = {"criteria": criteria}


#####################################################
## GENERATE AUTH AND REFRESH CODE

# # Generate Fresh Token
# auth_code = "1000.ea3db0812b8fd2ed3f6f55ab71b71735.59698dafdedb0ca672cf2cc4ef5beeed"
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

# # IMPORTANT: Use data=, not json=
# token_response = requests.post(post_url, data=token_data)

# print(token_response.status_code)
# print(token_response.json())

#####################################################

access_token = "1000.b195209a9be1175975ce67b0c470758a.59b7a87f1ec1d0aab5cae00a646a112b"
refresh_token = '1000.4144f1c17033fba3fea985e5050e1c2c.c3ced991667aad6fa884b424b7b7360e'
scope = 'ZohoCRM.modules.Leads.READ ZohoCRM.modules.Events.READ ZohoCRM.modules.Deals.READ'

# Get a Refresh Token
refresh_url = "https://accounts.zoho.in/oauth/v2/token"

data = {
    'refresh_token': refresh_token,
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'refresh_token'
}

response = requests.post(refresh_url, data=data)
new_tokens = response.json()

access_token = new_tokens.get('access_token')

#####################################################

# FETCH ZOHO LEADS DATA

get_url_leads = "https://www.zohoapis.in/crm/v8/Leads/search"

headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}

get_response = requests.get(get_url_leads, headers=headers, params=params)




# try:
# print(get_response.json())
# except Exception:
    # print("Raw Response Text:")
    # print(get_response.text)

raw_records = get_response.json().get('data', [])
df_leads_zoho = pd.json_normalize(raw_records)

#####################################################

#FETCH ZOHO DEALS DATA

get_url_deals = "https://www.zohoapis.in/crm/v8/Deals/search"

headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}

get_response = requests.get(get_url_deals, headers=headers, params=params)

print(f"Status Code: {get_response.status_code}")


# try:
# print(get_response.json())
# except Exception:
    # print("Raw Response Text:")
    # print(get_response.text)

raw_records = get_response.json().get('data', [])
df_deals_zoho = pd.json_normalize(raw_records)

#####################################################

#SETUP GOOGLE SHEETS

# 1. Authenticate using User Credentials (Client ID & Secret)
gc = gspread.oauth(
    credentials_filename='credentials.json',
    authorized_user_filename='authorized_user.json'  # Token is saved here automatically
)


# gc = gspread.service_account(filename="authorized_user.json")

sheet_url = "https://docs.google.com/spreadsheets/d/11_7I0Juswl_XWysMBL5CW2VXZ235AOxMGm-kEVtQPI4/edit?gid=0#gid=0"

sh = gc.open_by_url(sheet_url)

worksheet_leads = sh.worksheet("Leads")
worksheet_deals = sh.worksheet("Deals")

data_leads = worksheet_leads.get_all_records()
data_deals = worksheet_deals.get_all_records()

# set_with_dataframe(worksheet_leads, df_leads_zoho, row=1, col=1, include_index=False, include_column_header=True, resize=True)
# set_with_dataframe(worksheet_deals, df_deals_zoho, row=1, col=1, include_index=False, include_column_header=True, resize=True)

# Convert DF to list of lists; use .astype(str) to avoid JSON errors with dates
leads_data_to_append = df_leads_zoho.astype(str).values.tolist()
deals_data_to_append = df_deals_zoho.astype(str).values.tolist()

# 3. Append
worksheet_leads.append_rows(leads_data_to_append, value_input_option='USER_ENTERED')
worksheet_deals.append_rows(deals_data_to_append, value_input_option='USER_ENTERED')

#####################################################

worksheet_leads = sh.worksheet("Leads")
worksheet_deals = sh.worksheet("Deals")


#Filter data on the sheets out of duplicates
data_leads = pd.DataFrame(worksheet_leads.get_all_records())
data_deals = pd.DataFrame(worksheet_deals.get_all_records())

# 1. Ensure the date column is in datetime format
data_leads['Created_Time'] = pd.to_datetime(data_leads['Created_Time'])
data_deals['Created_Time'] = pd.to_datetime(data_deals['Created_Time'])

# 2. Sort by the ID and Date (ascending)
# This puts the newest record at the bottom for each ID
data_leads = data_leads.sort_values(['id', 'Created_Time'])
data_deals = data_deals.sort_values(['id', 'Created_Time'])

# 3. Drop duplicates, keeping only the last (newest) occurrence
data_leads = data_leads.drop_duplicates(subset='id', keep='last')
data_deals = data_deals.drop_duplicates(subset='id', keep='last')

set_with_dataframe(worksheet_leads, data_leads, row=1, col=1, include_index=False, include_column_header=True, resize=True)
set_with_dataframe(worksheet_deals, data_deals, row=1, col=1, include_index=False, include_column_header=True, resize=True)
