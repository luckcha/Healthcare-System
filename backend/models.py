from sqlalchemy import Column, String, ForeignKey
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True)
    name = Column(String)
    mobile = Column(String)
    age = Column(String)
    location = Column(String)
    photoshoot_by = Column(String)
    clinic = Column(String)


class Visit(Base):
    __tablename__ = "visits"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    date = Column(String)
    concern = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String)
    password = Column(String)