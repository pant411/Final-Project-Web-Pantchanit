# built in module
from flask import Flask, render_template, request, jsonify, make_response
# from werkzeug.utils import secure_filename
import cv2
import numpy as np

# my module
from mainModule import runMain # main application of project
from connectDB import update_data, find_all # connect to db

# UPLOAD_FOLDER = "/path/to/the/uploads"
# ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def mainPage():
    return "Hello World !!!!!"

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/uploadreceipt", methods = ["POST"])
def uploadReceipt():
    if request.method == "POST":  
        file = request.files["file"]
        image = cv2.imdecode(np.fromstring(file.read(), np.uint8),\
            cv2.IMREAD_UNCHANGED)
        path_file = "files/" + file.filename
        file.save(path_file)  
        shopName,shopPhone,taxIDShop,dateReceipt,receiptID = runMain(image)
        # print(shopName,shopPhone,taxIDShop,dateReceipt,receiptID)
        update_data(path_file,shopName,shopPhone,taxIDShop,dateReceipt,receiptID,collection="data")
        return "success"

@app.route("/listreceipt", methods = ["GET"])
def listReceipt():
    if request.method == "GET":  
        list_data = find_all(collection="data")
        # print(list_data)
        return {"data": list_data}

if __name__ == "__main__":
    app.run(debug=True, port=8788)