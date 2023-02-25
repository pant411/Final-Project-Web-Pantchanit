import requests
from dotenv import load_dotenv
import os

# load env vars
load_dotenv()

def main(type_receipt: int, file: any):

    url = os.getenv("URL_MAINSERVICE")
    r = requests.post(url = url, params={"type_receipt": type_receipt}, files={"file": file})
    return r.json()