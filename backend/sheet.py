import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(
    "credentials.json", scopes=SCOPES
)

client = gspread.authorize(creds)

SHEET_ID = "1nEIcAevIRa5h6Q_1zjeS4bQeGIxcMj6ZxNCTIt8WMY0"

sheet = client.open_by_key(SHEET_ID).sheet1


# 👤 ADD PATIENT (ONLY ONCE)
def add_patient(data):
    records = sheet.get_all_records()

    for r in records:
        if str(r["mobile"]) == str(data["mobile"]):
            return  # already exists

    sheet.append_row([
        data["patient_id"],
        data["name"],
        data["mobile"],
        data["age"],
        data["location"],
        data["photoshoot_by"],
        data["clinic"],
        data["folder_link"],
        "", "", ""
    ])


# 📅 UPDATE VISIT (NO DUPLICATE)
def add_visit(data):
    records = sheet.get_all_records()

    for i, row in enumerate(records, start=2):
        if str(row["mobile"]) == str(data["mobile"]):

            sheet.update(f"I{i}", [[data["date"]]])
            sheet.update(f"J{i}", [[data["concern"]]])
            sheet.update(f"K{i}", [[data["visit_id"]]])
            sheet.update(f"H{i}", [[data.get("folder_link", "")]])

            return


# 🔍 SEARCH
def search_patient(name):
    records = sheet.get_all_records()
    results = []

    for r in records:
        if name.lower() in r["name"].lower():
            results.append({
                "patient_id": r["patient_id"],
                "name": r["name"],
                "mobile": r["mobile"]
            })

    return results


# 🔍 FIND FOLDER
def find_patient_folder(mobile):
    records = sheet.get_all_records()

    for r in records:
        if str(r["mobile"]) == str(mobile):
            link = r.get("folder_link")
            if link:
                return link.split("/")[-1]

    return None