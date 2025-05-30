import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

sheet_id = os.environ["GOOGLE_SHEET_ID"]
credentials_dict = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

sheet = client.open_by_key(sheet_id)

# Ručně definovaný seznam listů, které se mají tahat
included_sheets = [
    "Airalo",
    "Yesim",
    "Mobimatter",
    "GlobalYO",
    "MayaMobile",
    "aloSIM",
    "eSIM4Travel",
    "Jetpac",
    "Airhub",
    "Saily",
    "Nomad",
    "Firsty",
    "eTravelSim",
    "Roamify"
]

# Mapa přejmenování sloupců
column_map = {
    "Country": "country",
    "Data (GB)": "data",
    "Validity (days)": "validity",
    "Provider": "provider",
    "Affiliate Link": "affiliate",
    "Data Range": "dataRange",
    "Validity Range": "validityRange",
    "Price": "price_usd"
}

combined_data = []

for title in included_sheets:
    ws = sheet.worksheet(title)
    rows = ws.get_all_values()
    headers = rows[0]
    for row in rows[1:]:
        entry = {}
        for i, value in enumerate(row):
            col_name = headers[i]
            key = column_map.get(col_name)
            if key:
                entry[key] = value
        if entry:
            combined_data.append(entry)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=2)
