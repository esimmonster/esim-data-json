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

# Zde si ručně udržuješ seznam povolených listů
included_sheets = [
    "Airalo",
    "Yesim",
    "Mobimatter",
    "GlobalYO",
    "MayaMobile",
    "eSIM4Travel",
    "Jetpac",
    "Airhub",
    "Saily",
    "Nomad",
    "Firsty",
    "aloSIM",
    "Roamify"
]

combined_data = []

for title in included_sheets:
    ws = sheet.worksheet(title)
    rows = ws.get_all_values()
    headers = rows[0]
    for row in rows[1:]:
        combined_data.append(dict(zip(headers, row)))

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=2)
