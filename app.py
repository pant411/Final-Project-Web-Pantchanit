# built in module
from fastapi import FastAPI, Request, File, UploadFile, status, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
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

@app.post("/receipts/create/", response_model=schemas.ResponseCreateReceipt)
async def createReceipt(receipt: schemas.ReceiptCreateMain, db: Session = Depends(get_db)):
    return crud.create_receipt_main(db=db, receipt=receipt)

@app.post("/receipts/analyze/", response_model=schemas.ResponseAnalyzeReceipt)
async def uploadReceipt(file: UploadFile, request: Request):
    image = cv2.imdecode(np.fromstring(file.file.read(), np.uint8),\
            cv2.IMREAD_UNCHANGED)
    # path_file = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)           
    path_file = "img/" + file.filename
    data = runMain(image)
    data["pathImage"] = "/static/"+path_file
    # print(data)
    # await file.seek(0)
    # with open("static/"+path_file, "wb+") as file_object:
    #     file_object.write(file.file.read())
    # redirect_url = request.url_for('home')   
    # return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return data

@app.get("/receipts/getOneByID/{receipt_id}", response_model=schemas.ResponseGetOneReceipt)
async def getOneReceipt(receipt_id: int, db: Session = Depends(get_db)):
    return crud.getOneReceipt_byDBId_main(db, receipt_id)

@app.get("/receipts/getByPagination", response_model=List[schemas.ResponseReceipt])
async def getReceiptByPagination(receipt_id: int, db: Session = Depends(get_db)):
    return crud.getReceiptByPagination(db, receipt_id)

