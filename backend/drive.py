from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import pickle

# 🔐 Permission
SCOPES = ['https://www.googleapis.com/auth/drive.file']


# 🔥 Get Drive Service (OAuth login)
def get_drive_service():
    creds = None

    # agar pehle login ho chuka hai
    if os.path.exists("token.pkl"):
        with open("token.pkl", "rb") as token:
            creds = pickle.load(token)

    # agar nahi hai to login karo
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.pkl", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)
    return service


# 📁 Create Main Folder (Patient)
def create_folder(folder_name):
    service = get_drive_service()

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()

    return folder.get('id')


# 📁 Create Subfolder (Pre / After / Visit)
def create_subfolder(folder_name, parent_id):
    service = get_drive_service()

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }

    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()

    return folder.get('id')


# 📤 Upload file inside folder
def upload_file(file_path, folder_id):
    service = get_drive_service()

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    return file.get('webViewLink')