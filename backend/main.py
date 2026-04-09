from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from uuid import uuid4
import shutil, os

from drive import create_folder, create_subfolder, upload_file

# 🆕 DB IMPORT
from database import SessionLocal, engine, Base
from models import Patient, Visit

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# 🔍 SEARCH (DB)
# -------------------------
@app.get("/search")
def search_patient(name: str):
    db = SessionLocal()

    patients = db.query(Patient).filter(
        Patient.name.contains(name)
    ).all()

    return [
        {
            "patient_id": p.id,
            "name": p.name,
            "mobile": p.mobile
        }
        for p in patients
    ]


# -------------------------
# 👤 CREATE PATIENT (DB)
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
    db = SessionLocal()

    patient_id = str(uuid4())

    folder_name = f"{name}_{mobile[-4:]}"
    folder_id = create_folder(folder_name)

    patient = Patient(
        id=patient_id,
        name=name,
        mobile=mobile,
        age=age,
        location=location,
        photoshoot_by=photoshoot_by,
        clinic=clinic
    )

    db.add(patient)
    db.commit()

    return {"patient_id": patient_id}


# -------------------------
# 📅 CREATE VISIT (DB)
# -------------------------
@app.post("/create-visit/{patient_id}")
def create_visit(
    patient_id: str,
    concern: str = Form(...),
    date: str = Form(...)
):
    db = SessionLocal()

    visit_id = str(uuid4())

    visit = Visit(
        id=visit_id,
        patient_id=patient_id,
        concern=concern,
        date=date
    )

    db.add(visit)
    db.commit()

    return {"visit_id": visit_id}


# -------------------------
# 📄 GET PATIENT
# -------------------------
@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    db = SessionLocal()

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    visits = db.query(Visit).filter(
        Visit.patient_id == patient_id
    ).all()

    return {
        "name": patient.name,
        "mobile": patient.mobile,
        "visits": [
            {
                "visit_id": v.id,
                "date": v.date,
                "concern": v.concern
            }
            for v in visits
        ]
    }


# -------------------------
# 📤 UPLOAD (same)
# -------------------------
@app.post("/upload/{patient_id}/{visit_id}")
def upload_files(
    patient_id: str,
    visit_id: str,
    folder_name: str = Form(...),
    files: List[UploadFile] = File(...)
):
    os.makedirs("temp", exist_ok=True)

    uploaded_links = []

    for file in files:
        path = f"temp/{file.filename}"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        link = upload_file(path, folder_name)
        uploaded_links.append(link)

        os.remove(path)

    return {"files": uploaded_links}


@app.get("/")
def home():
    return {"message": "Backend running 🚀"}