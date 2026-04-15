import os
import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(
    "/etc/secrets/credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

SHEET_ID = "1nEIcAevIRa5h6Q_1zjeS4bQeGIxcMj6ZxNCTIt8WMY0"
sheet = client.open_by_key(SHEET_ID).sheet1


# 🔍 SEARCH
def search_patient(name):
    data = sheet.get_all_records()
    return [row for row in data if name.lower() in row["name"].lower()]


# 🔍 FIND EXISTING PATIENT
def find_patient_folder(query):
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

# 👤 ADD PATIENT (ONLY ONCE)
def add_patient(data):
    sheet.append_row([
        data["patient_id"],
        data["name"],
        data["mobile"],
        data["age"],
        data["location"],
        data["photoshoot_by"],
        data["clinic"],
        data["patient_link"],   # column H
        "", "", "", "", ""      # बाकी खाली
    ])


# 📅 ADD VISIT
def add_visit(data):
    sheet.append_row([
        data["patient_id"],
        data["name"],
        data["mobile"],
        data.get("age", ""),
        data.get("location", ""),
        data.get("photoshoot_by", ""),
        data.get("clinic", ""),
        data["patient_link"],
        data["visit_link"],
        data["subfolder_link"],
        data["date"],
        data["concern"],
        data["visit_id"]
    ])
def get_all_patients():
    return sheet.get_all_records()    