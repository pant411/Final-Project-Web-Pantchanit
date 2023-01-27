# built in module
from fastapi import FastAPI, Request, File, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
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

@app.post("/uploadreceipt", response_class=HTMLResponse)
async def uploadReceipt(file: UploadFile, request: Request):
    image = cv2.imdecode(np.fromstring(file.file.read(), np.uint8),\
            cv2.IMREAD_UNCHANGED)
    # path_file = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)           
    path_file = "img/" + file.filename
    data = runMain(image)
    print(data)
    ObjID = insert_data(path_file,file.filename,data,collection="data")
    await file.seek(0)
    with open("static/"+path_file, "wb+") as file_object:
        file_object.write(file.file.read())
    # file.write("static/"+path_file) 
    redirect_url = request.url_for('home')   
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.route("/editreceipt", methods = ["PATCH"])
async def editReceipt():
    if Request.method == "PATCH": 
        body = Request.get_json()
        print(body)
        update_data(body, collection="data")

        return "success"
