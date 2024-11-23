from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import os, logging, io
from datetime import datetime
from dotenv import load_dotenv

log_stream = io.StringIO()
logging.basicConfig(level=logging.CRITICAL,
                    format= "%(asctime)s  %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    handlers=[logging.StreamHandler(log_stream)]
                    )

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACC_FILE = "service_account.json"
FOLDER_ID = os.getenv("FOLDER_ID")
LOG_ID = os.getenv("LOG_ID")

def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACC_FILE, scopes= SCOPES)
    return build("drive", "v3", credentials= creds)

def upload_file(file_stream):
    DRIVER_SERVICE =  authenticate()
    query = f"name='sales_data.db' and trashed=false"
    results = DRIVER_SERVICE.files().list(q=query, fields="files(id, parents)").execute()
    file_metadata = {'name': 'sales_data.db', "parents": [FOLDER_ID]}
    items = results.get("files", [])
    
    for item in items:
        if item["parents"][0] == FOLDER_ID:
            media = MediaIoBaseUpload(file_stream, mimetype='application/octet-stream')
            DRIVER_SERVICE.files().delete(fileId=item["id"]).execute()
            logging.info(f"File with ID: {item['id']} has been successfully deleted.")
            DRIVER_SERVICE.files().create(
                body=file_metadata,
                media_body=media).execute()
            logging.info(f"Sales Data file has been uploaded successfully.")
    
    
def upload_log():
    DRIVER_SERVICE = authenticate()
    log_stream.seek(0) 
    media = MediaIoBaseUpload(log_stream, mimetype="text/plain")
    DRIVER_SERVICE.files().update(
        fileId=LOG_ID,
        media_body=media
        ).execute()
    logging.info(f"Logger file has been uploaded successfully.")