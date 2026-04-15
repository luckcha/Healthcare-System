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
def find_patient_folder(mobile):
    data = sheet.get_all_records()
    for row in data:
        if str(row["mobile"]) == str(mobile):
            return row["patient_link"]
    return None


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
        "", "", "", "",   # skip patient info
        data["patient_link"],   # H
        data["visit_link"],     # I
        data["subfolder_link"], # J
        data["date"],           # K
        data["concern"],        # L
        data["visit_id"]        # M
    ])
def get_all_patients():
    return sheet.get_all_records()    