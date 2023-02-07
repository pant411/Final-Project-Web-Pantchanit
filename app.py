# built in module
from fastapi import FastAPI, Request, File, UploadFile, status, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from werkzeug.utils import secure_filename
import cv2
import numpy as np

# my module
from mainModule import runMain # main application of project

from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # list_data = find_all(collection="data")
    # print(list_data)
    # return render_template("home.html", list_data = list_data)
    return templates.TemplateResponse("home.html", {"request": request, "list_data": []})

@app.post("/receipts/", response_model=schemas.ResponseCreateReceipt)
async def create_receipt(receipt: schemas.ReceiptCreateMain, db: Session = Depends(get_db)):
    return crud.create_receipt_main(db=db, receipt=receipt)

@app.post("/uploadreceipt", response_class=HTMLResponse)
async def uploadReceipt(file: UploadFile, request: Request):
    image = cv2.imdecode(np.fromstring(file.file.read(), np.uint8),\
            cv2.IMREAD_UNCHANGED)
    # path_file = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)           
    path_file = "img/" + file.filename
    data = runMain(image)
    print(data)
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
        return "success"
