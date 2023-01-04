# built in module
from flask import Flask, render_template, request, jsonify, make_response
# from werkzeug.utils import secure_filename
import cv2
import numpy as np
import os

# my module
from mainModule import runMain # main application of project
from connectDB import update_data, find_all # connect to db

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
        file = request.files["image"]
        image = cv2.imdecode(np.fromstring(file.read(), np.uint8),\
            cv2.IMREAD_UNCHANGED)
        # path_file = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)           
        path_file = "img/" + file.filename
        shopName,shopPhone,taxIDShop,dateReceipt,receiptID = runMain(image)
        # print(shopName,shopPhone,taxIDShop,dateReceipt,receiptID)
        update_data(path_file,file.filename,shopName,shopPhone,\
            taxIDShop,dateReceipt,receiptID,collection="data")
        file.stream.seek(0)
        file.save("static/"+path_file) 
        return "success"

if __name__ == "__main__":
    app.run(debug=True, port=8788)