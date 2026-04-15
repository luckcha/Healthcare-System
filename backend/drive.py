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


# 🔥 MAKE PUBLIC FUNCTION
def make_public(file_id):
    service = get_drive_service()

    permission = {
        'type': 'anyone',
        'role': 'reader'
    }

    service.permissions().create(
        fileId=file_id,
        body=permission
    ).execute()


# 📁 CREATE MAIN FOLDER
def create_folder(name):
    service = get_drive_service()

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = service.files().create(
        body=file_metadata, fields='id'
    ).execute()

    folder_id = folder.get('id')

    make_public(folder_id)  # 🔥 IMPORTANT

    return folder_id


# 📁 CREATE SUBFOLDER
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

    folder_id = folder.get('id')

    make_public(folder_id)  # 🔥 IMPORTANT

    return folder_id


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


# 🔗 GET LINK
def get_folder_link(folder_id):
    return f"https://drive.google.com/drive/folders/{folder_id}"

def extract_folder_id(link):
    return link.split("/")[-1]