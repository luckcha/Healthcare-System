from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from uuid import uuid4
import shutil, os

from drive import (
    create_folder,
    create_subfolder,
    upload_file,
    get_folder_link,
    extract_folder_id
)

from sheet import add_patient, add_visit, find_patient_folder

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production me domain dal dena
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ ROOT
@app.get("/")
def home():
    return {"message": "Backend Running 🚀"}


# 🔍 SEARCH API (🔥 NEW ADD)
@app.get("/search-patient")
def search_patient(query: str = Query(...)):
    return find_patient_folder(query, search=True)


# 🧾 CREATE FULL FLOW
@app.post("/create-full")
def create_full(
    name: str = Form(...),
    mobile: str = Form(...),
    age: str = Form(...),
    location: str = Form(...),
    photoshoot_by: str = Form(...),
    clinic: str = Form(...),
    concern: str = Form(...),
    date: str = Form(...),
    subfolder_name: str = Form(...),
    files: List[UploadFile] = File(...)
):
    patient_id = str(uuid4())
    visit_id = str(uuid4())

    # 🔍 CHECK EXISTING PATIENT
    existing_folder = find_patient_folder(mobile)

    if existing_folder:
        patient_folder_id = extract_folder_id(existing_folder)
        patient_link = existing_folder
    else:
        patient_folder_id = create_folder(f"{name}_{mobile[-4:]}")
        patient_link = get_folder_link(patient_folder_id)

        add_patient({
            "patient_id": patient_id,
            "name": name,
            "mobile": mobile,
            "age": age,
            "location": location,
            "photoshoot_by": photoshoot_by,
            "clinic": clinic,
            "folder_link": patient_link
        })

    # 📁 VISIT FOLDER
    visit_folder_id = create_subfolder(f"Visit_{date}", patient_folder_id)
    visit_link = get_folder_link(visit_folder_id)

    # 📂 SUBFOLDER
    subfolder_id = create_subfolder(subfolder_name, visit_folder_id)
    subfolder_link = get_folder_link(subfolder_id)

    # 📤 FILE UPLOAD
    os.makedirs("temp", exist_ok=True)

    for file in files:
        path = f"temp/{file.filename}"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        upload_file(path, subfolder_id)
        os.remove(path)

    # 📝 SAVE VISIT
    add_visit({
        "patient_id": patient_id,
        "name": name,
        "mobile": mobile,
        "date": date,
        "concern": concern,
        "visit_id": visit_id,
        "patient_link": patient_link,
        "visit_link": visit_link,
        "subfolder_link": subfolder_link
    })

    return {"message": "Success 🚀"}