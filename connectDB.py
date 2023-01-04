import pymongo
import os

# env
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

MONGO_URL = os.getenv("MONGO_URL")
NAME_DB = os.getenv("NAME_DB")

myclient = pymongo.MongoClient(MONGO_URL,\
     tls=True, tlsAllowInvalidCertificates=True)

mydb = myclient[NAME_DB]

def update_data(pathImage: str, shopName: str, shopPhone: str,\
    taxIDShop: str, dateReceipt: str, receiptID: str, collection: str):
    mycol = mydb[collection]
    new_data = {
        "pathImage": pathImage,
        "shopName": shopName, 
        "shopPhone": shopPhone, 
        "taxIDShop": taxIDShop, 
        "dateReceipt": dateReceipt, 
        "receiptID": receiptID
    }
    mycol.insert_one(new_data)
    # return x

def find_all(collection: str):
    results = []
    mycol = mydb[collection]
    list_data = mycol.find()
    for ele in list_data:
        ele['_id'] = str(ele['_id'])
        results.append(ele)        
    return results
