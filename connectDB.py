import pymongo
import os
from bson import ObjectId

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

def insert_data(pathImage: str, filename: str, shopName: str, shopPhone: str,\
    taxIDShop: str, dateReceipt: str, receiptID: str, collection: str):
    mycol = mydb[collection]
    new_data = {
        "pathImage": pathImage,
        "filename": filename,
        "shopName": shopName, 
        "shopPhone": shopPhone, 
        "taxIDShop": taxIDShop, 
        "dateReceipt": dateReceipt, 
        "receiptID": receiptID
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