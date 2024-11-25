from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import os, logging, io
import json
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
data = json.loads(os.getenv("SERVICE_ACC"))
LOG_ID = os.getenv("LOG_ID")
FOLDER_ID = os.getenv("FOLDER_ID")
FILE_ID = os.getenv("FILE_ID")

# Create a google service
def authenticate():
    creds = service_account.Credentials.from_service_account_info(
        data, scopes= SCOPES)
    return build("drive", "v3", credentials= creds)

# 
def upload_file(file_stream):
    DRIVER_SERVICE =  authenticate()
    media = MediaIoBaseUpload(file_stream, mimetype='application/octet-stream')
    DRIVER_SERVICE.files().update(
        fileId=FILE_ID,
        media_body=media).execute()
    logging.info(f"Sales Data file has been uploaded successfully.")
   
#    
def upload_log():
    DRIVER_SERVICE = authenticate()
    log_stream.seek(0) 
    media = MediaIoBaseUpload(log_stream, mimetype="text/plain")
    DRIVER_SERVICE.files().update(
        fileId=LOG_ID,
        media_body=media
        ).execute()
    logging.info(f"Logger file has been uploaded successfully.")