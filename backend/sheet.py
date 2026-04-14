import os
import json
import gspread
from google.oauth2.service_account import Credentials

# ==============================
# 🔐 GOOGLE AUTH (ENV BASED)
# ==============================

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds_dict = json.loads(os.environ["GOOGLE_CREDS"])

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=SCOPES
)

client = gspread.authorize(creds)

SHEET_ID = "PASTE_YOUR_SHEET_ID"

sheet = client.open_by_key(SHEET_ID).sheet1


# ==============================
# 🔍 SEARCH PATIENT
# ==============================

def search_patient(name):
    data = sheet.get_all_records()

    result = []

    for row in data:
        if name.lower() in row["name"].lower():
            result.append({
                "patient_id": row["patient_id"],
                "name": row["name"],
                "mobile": row["mobile"],
                "folder_link": row["folder_link"]
            })

    return result


# ==============================
# 🔍 FIND EXISTING PATIENT FOLDER
# ==============================

def find_patient_folder(mobile):
    data = sheet.get_all_records()

    for row in data:
        if str(row["mobile"]) == str(mobile):
            return row["folder_link"]

    return None


# ==============================
# 👤 ADD PATIENT (NO DUPLICATE)
# ==============================

def add_patient(data):
    existing = find_patient_folder(data["mobile"])

    # ❌ already exists → skip
    if existing:
        return False

    sheet.append_row([
        data["patient_id"],
        data["name"],
        data["mobile"],
        data["age"],
        data["location"],
        data["photoshoot_by"],
        data["clinic"],
        data["folder_link"],
        "", "", ""   # date, concern, visit_id empty
    ])

    return True


# ==============================
# 📅 ADD VISIT
# ==============================

def add_visit(data):
    sheet.append_row([
        data["patient_id"],
        data["name"],
        data["mobile"],
        "", "", "", "",   # age, location, etc empty
        data.get("folder_link", ""),
        data["date"],
        data["concern"],
        data["visit_id"]
    ])