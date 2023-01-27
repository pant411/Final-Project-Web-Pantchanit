# built in module
# from flask import Flask, render_template, request, redirect, url_for
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from werkzeug.utils import secure_filename
import cv2
import numpy as np

# my module
from mainModule import runMain # main application of project
from connectDB import insert_data, find_all, update_data # connect to db

# UPLOAD_FOLDER = "img-receipt"
# ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

# app = Flask(__name__)
app = FastAPI()
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    list_data = find_all(collection="data")
    print(list_data)
    # return render_template("home.html", list_data = list_data)
    return templates.TemplateResponse("home.html", {"request": request, "list_data": list_data})

@app.post("/uploadreceipt")
async def uploadReceipt(file: UploadFile):
    image = cv2.imdecode(np.fromstring(file.file.read(), np.uint8),\
            cv2.IMREAD_UNCHANGED)
    # path_file = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)           
    path_file = "img/" + file.filename
    shopName,shopPhone,taxIDShop,dateReceipt,receiptID = runMain(image)
    # print(shopName,shopPhone,taxIDShop,dateReceipt,receiptID)
    ObjID = insert_data(path_file,file.filename,shopName,shopPhone,\
        taxIDShop,dateReceipt,receiptID,collection="data")
    await file.seek(0)
    with open("static/"+path_file, "wb+") as file_object:
        file_object.write(file.file.read())
    # file.write("static/"+path_file) 
    # return redirect(url_for('home'))
    return {
        "_id": ObjID,
        "pathImage": path_file,
        "filename": file.filename,
        "receiptID": receiptID,
        "dateReceipt": dateReceipt,
        "shopName": shopName,
        "shopPhone": shopPhone,
        "taxIDShop": taxIDShop,
    }

@app.route("/editreceipt", methods = ["PATCH"])
async def editReceipt():
    if Request.method == "PATCH": 
        body = Request.get_json()
        print(body)
        update_data(body, collection="data")

        return "success"
    
"""
if __name__ == "__main__":
    app.run(debug=True, port=8788)

"""
