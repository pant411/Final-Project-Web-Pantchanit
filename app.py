# built in module
from typing import List
from fastapi import FastAPI, Request, File, UploadFile, status, Depends, HTTPException, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_pagination import Page, paginate, add_pagination
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
# from werkzeug.utils import secure_filename
import cv2
import numpy as np
from datetime import datetime

# my module
from mainModule import runMain # main application of project

from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Final Project", debug=True)

add_pagination(app)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Dependency
def get_db(request: Request):
    return request.state.db

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


#################################### Template Module #################################### 

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/addreceipt", response_class=HTMLResponse)
def addreceipt(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

@app.get("/receiptdetail/{receipt_id}", response_class=HTMLResponse)
async def receiptdetail(receipt_id: int, request: Request,
                        db: Session = Depends(get_db)):
    receipt_data = await crud.getOneReceipt_byDBId_main(db, receipt_id)
    db_item = await crud.getItem_byDBId(db, owner_receiptId = receipt_id)
    print(receipt_data)
    return templates.TemplateResponse("receiptdetail.html", {
        "request": request, 
        "receipt_data": receipt_data, 
        "items": db_item})

@app.get("/listreceipts", response_class=HTMLResponse)
async def getlistReceiptAllPage(request: Request, db: Session = Depends(get_db)):
    list_data = await crud.getReceiptByAll(db)
    return templates.TemplateResponse("listReceipt.html", {
        "request": request, 
        "list_data": list_data})

@app.get("/listshops", response_class=HTMLResponse)
async def getlistShopByPagination(request: Request, db: Session = Depends(get_db)):
    list_data = await crud.getShopAll(db)
    return templates.TemplateResponse("listShop.html", {
        "request": request, 
        "list_data": list_data})

@app.get("/listcustomers", response_class=HTMLResponse)
async def getlistCustomerByPagination(request: Request, 
                                      db: Session = Depends(get_db)):
    list_data = await crud.getCustomerAll(db)
    return templates.TemplateResponse("listCustomer.html", {
        "request": request, 
        "list_data": list_data})

@app.get("/checkreceipt/{receipt_id}", response_class=HTMLResponse)
async def checkreceipt(receipt_id: int, request: Request, db: Session = Depends(get_db)):
    receipt_data = await crud.getOneReceipt_byDBId_main(db, receipt_id)
    db_item = await crud.getItem_byDBId(db, owner_receiptId = receipt_id)
    return templates.TemplateResponse("checkReceipt.html", {
        "request": request,
        "receipt_data": receipt_data, 
        "items": db_item})

@app.get("/editreceipt/{receipt_id}", response_class=HTMLResponse)
async def editreceipt(receipt_id: int,
                      request: Request, 
                      db: Session = Depends(get_db)):
    receipt_data = await crud.getOneReceipt_byDBId_main(db, receipt_id)
    db_item = await crud.getItem_byDBId(db, owner_receiptId = receipt_id)
    return templates.TemplateResponse("editReceipt.html", {
        "request": request, 
        "receipt_data": receipt_data, 
        "items": db_item})

#################################### Receipt Module #################################### 

@app.post("/receipts/create/", tags = ["Receipts"], 
          response_model=schemas.ResponseCreateReceipt)
async def createReceipt(receipt: schemas.ReceiptCreateMain, 
                        db: Session = Depends(get_db)):
    return await crud.create_receipt_main(db=db, receipt=receipt)

@app.post("/receipts/submit", tags = ["Receipts"])
async def submitReceipt(request: Request,
                        type_receipt: int = Form(...), 
                        file: UploadFile = File(...), 
                        db: Session = Depends(get_db)):
    # print("tuuu",type_receipt)
    content_receipt = file.file.read()
    image = cv2.imdecode(np.fromstring(content_receipt, np.uint8),\
            cv2.IMREAD_UNCHANGED)
    # path_file = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)           
    data = runMain(image, type_receipt)
    path_file = "img/" + file.filename
    data["pathImage"] = path_file
    data["filename"] = file.filename
    # print(data["dateReceipt"])
    # print(data)
    db_receipt = await crud.create_receipt_main(db=db, receipt=data, type_receipt=type_receipt)
    print(db_receipt)
    await file.seek(0)
    with open("static/"+path_file, "wb+") as file_object:
        file_object.write(content_receipt)
    redirect_url = request.url_for('checkreceipt', **{"receipt_id": db_receipt.id})   
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    # return data


@app.post("/receipts/submitreceipt", tags = ["Receipts"])
async def submitReceipt2(request: Request,
                         type_receipt: int = Form(...), 
                         file: UploadFile = File(...)):
    # print("tuuu",type_receipt)
    content_receipt = file.file.read()
    print(content_receipt)
    image = cv2.imdecode(np.fromstring(content_receipt, np.uint8),\
            cv2.IMREAD_UNCHANGED)
    # path_file = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)           
    data = runMain(image, type_receipt)
    path_file = "img/" + file.filename
    data["pathImage"] = path_file
    data["filename"] = file.filename
    # data["receipt-content"] = content_receipt
    # redirect_url = request.url_for('checkreceipt')   
    # return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return data

@app.get("/receipts/getOneByID/{receipt_id}", 
         tags = ["Receipts"], 
         response_model=schemas.ResponseGetOneReceipt)
async def getOneReceipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = crud.getOneReceiptByID(db, id = receipt_id)
    if db_receipt is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt not found with the given ID")
    return await crud.getOneReceipt_byDBId_main(db, receipt_id)

@app.get("/receipts/getByPagination/", 
         tags = ["Receipts"], 
         response_model=Page[schemas.ResponseReceiptAll])
async def getReceiptByPagination(db: Session = Depends(get_db)):
    return await paginate(crud.getReceiptByAll(db))

@app.get('/receipts/deleteReceiptByID/{receipt_id}', 
            tags = ["Receipts"])
async def removeOneReceipt_byIndex(request: Request,receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = await crud.getOneReceiptByID(db, id = receipt_id)
    if db_receipt is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt not found with the given ID")
    await crud.removeOneReceipt_byIndex(db, id = receipt_id)
    redirect_url = request.url_for('listreceipts')   
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

@app.get("/receipts/getItemAll/{receipt_id}", tags = ["Receipts"])
async def getItemAll(receipt_id: int, db: Session = Depends(get_db)):
    return await crud.getItem_byDBId(db, owner_receiptId=receipt_id)

@app.patch("/receipts/editoneitem/{receipt_id}/{item_id}", tags = ["Receipts"])
async def editOneItem(receipt_id: int, item_id: int, data_item: schemas.EditItem, db: Session = Depends(get_db)):
    # db_item = await crud.getOneItem_byDBId(db, owner_receiptId=receipt_id, item_id=item_id)
    db_item_query = db.query(models.Item).filter_by(
        owner_receiptId = receipt_id,
        id = item_id)
    db_item = db_item_query.first()
    if db_item is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt and Item not found with the given ID")  
    update_data = data_item.dict(exclude_unset=True) 
    db_item_query.filter(models.Item.id == item_id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_item)
    return db_item

#################################### Shop Module #################################### 

@app.get("/shops/getShopAll", 
         tags = ["shops"], 
         response_model=Page[schemas.ResponseShopAll])
async def getShopAll(db: Session = Depends(get_db)):
    return await paginate(crud.getShopAll(db))

#################################### Customer Module #################################### 

@app.get("/customers/getCustomerAll", 
         tags = ["customers"], 
         response_model=Page[schemas.ResponseCustomerAll])
async def getCustomerAll(db: Session = Depends(get_db)):
    return await paginate(crud.getCustomerAll(db))
