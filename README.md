# 🏥 Healthcare Patient Management System

A full-stack healthcare application to manage patient records, visit history, and medical media (images/videos) using Google Drive integration.

---

## 🚀 Features

### 👤 Patient Management

* Create new patients with details:

  * Name
  * Mobile Number (unique)
  * Age
  * Location
  * Photoshoot Done By
  * Clinic Location (Gurugram / Pitampura)
* Search patients with **auto-suggestion**
* Handle duplicate names using mobile number

---

### 📅 Visit Tracking

* Track multiple visits per patient
* Store:

  * Visit date
  * Concern
  * History per visit
* Organized visit-based records

---

### 📁 Google Drive Integration

* Auto-create folder per patient
* Create subfolders:

  * Pre / Before / After / Custom
* Upload **multiple images/videos**
* All media stored in Google Drive

---

### 📤 Media Upload

* Upload multiple files at once
* Folder-based organization
* Structured storage:

  ```
  Patient_Name/
      Visit_2026-04-04/
          Pre/
          After/
  ```

---

### 🔍 Smart Search (Auto Suggestion)

* Type patient name
* Instant suggestions appear
* Click to open patient profile

---

### 🎨 Modern UI

* Clean dashboard design
* Card-based layout
* Dropdowns & smooth UX
* Responsive structure

---

## 🛠️ Tech Stack

### Frontend

* React.js
* Axios
* CSS (Custom UI)

### Backend

* FastAPI (Python)
* Uvicorn

### Storage

* Google Drive API

---

## 📁 Project Structure

```
healthcare-system/
│
├── backend/
│   ├── main.py
│   ├── drive.py
│   ├── client_secret.json (ignored)
│   ├── token.pkl (ignored)
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   ├── Patient.js
│   │   ├── App.js
│   │   ├── index.css
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/Healthcare-System.git
cd Healthcare-System
```

---

### 2️⃣ Backend Setup

```
cd backend
pip install fastapi uvicorn google-api-python-client google-auth google-auth-oauthlib
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### 3️⃣ Frontend Setup

```
cd frontend
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## 🔐 Environment Setup

⚠️ Do NOT upload these files to GitHub:

* `client_secret.json`
* `credentials.json`
* `token.pkl`

Add your own Google API credentials:

1. Go to Google Cloud Console
2. Enable Drive API
3. Download OAuth credentials
4. Place inside `/backend`

---

## 📸 How It Works

1. Search or create a patient
2. Create a visit
3. Upload files (Pre / After etc.)
4. Files automatically stored in Google Drive

---

## 🎯 Future Improvements

* Database integration (PostgreSQL / SQLite)
* Image preview gallery
* Before/After comparison slider
* Authentication system
* Admin dashboard
* Analytics & reports

---

## 💡 Use Cases

* Dermatology clinics
* Hair treatment clinics
* Aesthetic centers
* Medical record management

---



## ⭐ Show your support

If you like this project, give it a ⭐ on GitHub!

---
