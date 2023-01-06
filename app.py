# built in module
from flask import Flask, render_template, request, redirect, url_for
# from werkzeug.utils import secure_filename
import cv2
import numpy as np

# my module
from mainModule import runMain # main application of project
from connectDB import insert_data, find_all, update_data # connect to db

# UPLOAD_FOLDER = "img-receipt"
# ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    list_data = find_all(collection="data")
    print(list_data)
    return render_template("home.html", list_data = list_data)

@app.route("/uploadreceipt", methods = ["POST"])
def uploadReceipt():
    if request.method == "POST": 
        file = request.files["up-image"]
        image = cv2.imdecode(np.fromstring(file.read(), np.uint8),\
            cv2.IMREAD_UNCHANGED)
        # path_file = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)           
        path_file = "img/" + file.filename
        shopName,shopPhone,taxIDShop,dateReceipt,receiptID = runMain(image)
        # print(shopName,shopPhone,taxIDShop,dateReceipt,receiptID)
        ObjID = insert_data(path_file,file.filename,shopName,shopPhone,\
            taxIDShop,dateReceipt,receiptID,collection="data")
        file.stream.seek(0)
        file.save("static/"+path_file) 
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
def editReceipt():
    if request.method == "PATCH": 
        body = request.get_json()
        print(body)
        update_data(body, collection="data")

        return "success"

if __name__ == "__main__":
    app.run(debug=True, port=8788)