import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

CLIENT_SECRET_PATH = os.path.join(PROJECT_ROOT, "client_secret.json")
TOKEN_PATH = os.path.join(PROJECT_ROOT, "token.pickle")


def get_authenticated_service():
    creds = None

    if os.path.exists(TOKEN_PATH):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_PATH,
            SCOPES
        )
            
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)


def upload_video(file_path, title, description):
    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["shorts"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(file_path)
    )

    response = request.execute()
    return response["id"]