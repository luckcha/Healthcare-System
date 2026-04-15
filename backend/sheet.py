import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# 🔥 Render Secret File
with open("/etc/secrets/credentials.json") as f:
    creds_json = json.load(f)

creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)

client = gspread.authorize(creds)
SHEET_ID = "1nEIcAevIRa5h6Q_1zjeS4bQeGIxcMj6ZxNCTIt8WMY0"

sheet = client.open_by_key(SHEET_ID).sheet1


# 🧑 ADD PATIENT
def add_patient(data):
    sheet.append_row([
        data["patient_id"],
        data["name"],
        data["mobile"],
        data["age"],
        data["location"],
        data["photoshoot_by"],
        data["clinic"],
        data["folder_link"],  # H
        "", "", "", "", "", ""
    ])


# 📅 ADD VISIT
def add_visit(data):
    sheet.append_row([
        data["patient_id"],
        data["name"],
        data["mobile"],
        "", "", "", "",  # skip patient columns
        data["patient_link"],   # H
        data["visit_link"],     # I
        data["subfolder_link"], # J
        data["date"],           # K
        data["concern"],        # L
        data["visit_id"]        # M
    ])


# 🔍 FIND PATIENT (🔥 FIXED)
def find_patient_folder(mobile):
    records = sheet.get_all_records()

    for row in records:
        if str(row.get("mobile")) == str(mobile):
            return row.get("patient_link")  # only string

    return None


# 🔎 SEARCH PATIENT
def search_patient(query):
    records = sheet.get_all_records()
    results = []

    for row in records:
        name = str(row.get("name", "")).lower()
        mobile = str(row.get("mobile", ""))

        if query.lower() in name or query in mobile:
            results.append({
                "patient_id": row.get("patient_id"),
                "name": row.get("name"),
                "mobile": row.get("mobile"),
                "patient_link": row.get("patient_link")
            })

    return results