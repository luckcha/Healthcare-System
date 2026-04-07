from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from uuid import uuid4
import shutil
import os

from drive import create_folder, create_subfolder, upload_file

app = FastAPI()

# CORS (frontend connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory DB
patients = {}

# -------------------------
# 🔍 SEARCH PATIENT
# -------------------------
@app.get("/search")
def search_patient(name: str):
    results = []

    for pid, p in patients.items():
        if name.lower() in p["name"].lower():
            results.append({
                "patient_id": pid,
                "name": p["name"],
                "mobile": p["mobile"]
            })

    return results


# -------------------------
# 👤 CREATE PATIENT
# -------------------------
@app.post("/create-patient")
def create_patient(
    name: str = Form(...),
    mobile: str = Form(...),
    age: str = Form(...),
    location: str = Form(...),
    photoshoot_by: str = Form(...),
    clinic: str = Form(...)
):
    patient_id = str(uuid4())

    folder_name = f"{name}_{mobile[-4:]}"
    folder_id = create_folder(folder_name)

    patients[patient_id] = {
        "name": name,
        "mobile": mobile,
        "age": age,
        "location": location,
        "photoshoot_by": photoshoot_by,
        "clinic": clinic,
        "folder_id": folder_id,
        "visits": []
    }

    return {
        "patient_id": patient_id,
        "message": "Patient created"
    }


# -------------------------
# 📅 CREATE VISIT
# -------------------------
@app.post("/create-visit/{patient_id}")
def create_visit(
    patient_id: str,
    concern: str = Form(...),
    date: str = Form(...)
):
    if patient_id not in patients:
        return {"error": "Invalid patient"}

    visit_id = str(uuid4())

    # create visit folder
    visit_folder_name = f"Visit_{date}"
    visit_folder_id = create_subfolder(
        visit_folder_name,
        patients[patient_id]["folder_id"]
    )

    visit = {
        "visit_id": visit_id,
        "date": date,
        "concern": concern,
        "folder_id": visit_folder_id,
        "subfolders": {}
    }

    patients[patient_id]["visits"].append(visit)

    return {
        "visit_id": visit_id,
        "message": "Visit created"
    }


# -------------------------
# 📤 UPLOAD FILES
# -------------------------
@app.post("/upload/{patient_id}/{visit_id}")
def upload_files(
    patient_id: str,
    visit_id: str,
    folder_name: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if patient_id not in patients:
        return {"error": "Invalid patient"}

    patient = patients[patient_id]

    visit = next(
        (v for v in patient["visits"] if v["visit_id"] == visit_id),
        None
    )

    if not visit:
        return {"error": "Visit not found"}

    # create subfolder if not exists
    if folder_name not in visit["subfolders"]:
        subfolder_id = create_subfolder(
            folder_name,
            visit["folder_id"]
        )
        visit["subfolders"][folder_name] = subfolder_id

    folder_id = visit["subfolders"][folder_name]

    os.makedirs("temp", exist_ok=True)

    uploaded_links = []

    for file in files:
        file_path = f"temp/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        link = upload_file(file_path, folder_id)
        uploaded_links.append(link)

        os.remove(file_path)

    return {"files": uploaded_links}


# -------------------------
# 📄 GET PATIENT DETAILS
# -------------------------
@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    return patients.get(patient_id)


# -------------------------
# 🏠 ROOT CHECK
# -------------------------
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}