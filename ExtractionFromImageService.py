import requests
from dotenv import load_dotenv
import os

# load env vars
load_dotenv()

def main_service(file: any):

    url = os.getenv("URL_MAINSERVICE")
    r = requests.post(
        url = url + "/receipts/file/submitreceipt",
        files={"file": file})
    return r.json()