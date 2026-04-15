from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os, pickle

SCOPES = ['https://www.googleapis.com/auth/drive']


def get_drive_service():
    creds = None

    if os.path.exists("token.pkl"):
        with open("token.pkl", "rb") as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.pkl", "wb") as token:
            pickle.dump(creds, token)

    return build("drive", "v3", credentials=creds)


# 🔥 IMPORTANT FIX
def extract_folder_id(link):
    if "folders/" in link:
        return link.split("folders/")[1].split("?")[0]
    return link


def create_folder(name):
    service = get_drive_service()

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = service.files().create(
        body=file_metadata, fields='id'
    ).execute()

    return folder.get('id')


def create_subfolder(name, parent_id):
    service = get_drive_service()

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }

    folder = service.files().create(
        body=file_metadata, fields='id'
    ).execute()

    return folder.get('id')


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


def get_folder_link(folder_id):
    return f"https://drive.google.com/drive/folders/{folder_id}"