import pymongo
import os
from bson import ObjectId
from bson.timestamp import Timestamp
import datetime as dt

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

def insert_data(pathImage: str, filename: str, data: any, collection: str):
    timestamp = Timestamp(int(dt.datetime.today().timestamp()), 1)
    mycol = mydb[collection]
    new_data = {
        "pathImage": pathImage,
        "filename": filename,
        "shopName": data["shopName"], 
        "shopPhone": data["shopPhone"], 
        "taxIDShop": data["taxIDShop"], 
        "dateReceipt": data["dateReceipt"], 
        "receiptID": data["receiptID"],
        "address-shop": data["address-shop"],
        "address-customer": data["address-customer"] ,
        "timestamp": timestamp
    }
    res = mycol.insert_one(new_data)
    ObjId = str(res.inserted_id)
    return ObjId

def find_all(collection: str):
    results = []
    mycol = mydb[collection]
    list_data = mycol.find()
    for ele in list_data:
        ele['_id'] = str(ele['_id'])
        results.append(ele)        
    return results

def update_data(body: any, collection: str):
    mycol = mydb[collection]
    myquery = { "_id": ObjectId(body["_id"]) }
    del body["_id"]
    newvalues = { "$set": body }
    mycol.update_one(myquery, newvalues)
