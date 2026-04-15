from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

SCOPES = ['https://www.googleapis.com/auth/drive']


# 🔐 SERVICE ACCOUNT AUTH (PRODUCTION)
def get_drive_service():
    creds = Credentials.from_service_account_file(
        "/etc/secrets/credentials.json",   # 🔥 Render secret file
        scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


# 📁 CREATE MAIN FOLDER
def create_folder(name):
    service = get_drive_service()

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()

    return folder.get('id')


# 📁 CREATE SUBFOLDER
def create_subfolder(name, parent_id):
    service = get_drive_service()

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }

    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()

    return folder.get('id')


# 📤 UPLOAD FILE
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
        fields='webViewLink'
    ).execute()

    return file.get('webViewLink')


# 🔗 GET FOLDER LINK
def get_folder_link(folder_id):
    return f"https://drive.google.com/drive/folders/{folder_id}"


# 🔧 EXTRACT ID FROM LINK
def extract_folder_id(link):
    return link.split("/")[-1]