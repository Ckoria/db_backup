import requests, logging
import os, io
from dotenv import load_dotenv
from google_access import upload_file, upload_log
from datetime import datetime
load_dotenv()

token = os.getenv("PAW_API_KEY")
file_url = os.getenv("URL")
try:
    headers = {'Authorization': f'Token {token}'}
except Exception as e:
    logging.error("Error occurred ", e)

def download_file():
    logging.info("Downloading...")
    try:
        response = requests.get(file_url, headers=headers)
        if response.status_code == 200:
            file_stream = io.BytesIO(response.content)
            file_stream.seek(0) 
            logging.info("Finished downloading the file.")
            upload_file(file_stream)
            upload_log()
        else:
            logging.ERROR('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
    except Exception as e:
        logging.error(e)    
    