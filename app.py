# built in module
from typing import List, Union
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

@app.get("/checkreceipt/{receipt_id}", response_class=HTMLResponse)
async def checkreceipt(receipt_id: int, request: Request, db: Session = Depends(get_db)):
    receipt_data = await crud.getOneReceipt_byDBId_main(db, receipt_id)
    db_item = await crud.getItem_byDBId(db, owner_receiptId = receipt_id)
    return templates.TemplateResponse("EditAndCheckReceipt.html", {
        "request": request,
        "receipt_data": receipt_data, 
        "items": db_item,
        "status": "process"})

@app.get("/editreceipt/{receipt_id}", response_class=HTMLResponse)
async def editreceipt(receipt_id: int,
                      request: Request, 
                      db: Session = Depends(get_db)):
    receipt_data = await crud.getOneReceipt_byDBId_main(db, receipt_id)
    db_item = await crud.getItem_byDBId(db, owner_receiptId = receipt_id)
    return templates.TemplateResponse("EditAndCheckReceipt.html", {
        "request": request, 
        "receipt_data": receipt_data, 
        "items": db_item,
        "status": "process"})

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
    print(data)
    db_receipt = await crud.create_receipt_main(db=db, 
                                                receipt=data, 
                                                type_receipt=type_receipt)
    # print(db_receipt)
    await file.seek(0)
    with open("static/"+path_file, "wb+") as file_object:
        file_object.write(content_receipt)
    redirect_url = request.url_for('editreceipt', **{"receipt_id": db_receipt.id})   
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    # return data

@app.post("/receipts/submitreceipt", tags = ["Receipts"])
async def submitReceipt2(type_receipt: int = Form(...), 
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

@app.delete('/receipts/deleteReceiptByID/{receipt_id}', 
            tags = ["Receipts"])
async def removeOneReceipt_byIndex(receipt_id: int, 
                                   db: Session = Depends(get_db)):
    db_receipt = await crud.getOneReceiptByID(db, id = receipt_id)
    if db_receipt is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt not found with the given ID")
    await crud.removeOneReceipt_byIndex(db, id = receipt_id)
    return {"success": True}

@app.delete('/receipts/deleteitem/{receipt_id}/{item_id}', 
            tags = ["Receipts"])
async def removeOneItemByIndex(receipt_id: int, 
                               item_id: int, 
                               db: Session = Depends(get_db)):
    db_item = await crud.getOneItem_byDBId(db, owner_receiptId = receipt_id, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt not found with the given ID")
    await crud.removeOneItemByIndex(db, id = item_id, owner_receiptId=receipt_id)
    return {"success": True}

@app.delete('/receipts/deletemanyitem/{receipt_id}', 
            tags = ["Receipts"])
async def removeManyItemByIndex(receipt_id: int, 
                               deleteItem: schemas.DeleteManyItem, 
                               db: Session = Depends(get_db)):
    for ele in deleteItem.listDelete:
        await crud.removeOneItemByIndex(db, id = ele, owner_receiptId=receipt_id)
    return {"success": True}

@app.get("/receipts/getItemAll/{receipt_id}", tags = ["Receipts"])
async def getItemAll(receipt_id: int, db: Session = Depends(get_db)):
    return await crud.getItem_byDBId(db, owner_receiptId=receipt_id)

@app.patch("/receipts/editoneitem/{receipt_id}/{item_id}", tags = ["Receipts"])
async def editOneItem(receipt_id: int, 
                      item_id: int, 
                      data_item: schemas.EditItem, 
                      db: Session = Depends(get_db)):
    # db_item = await crud.getOneItem_byDBId(db, owner_receiptId=receipt_id, item_id=item_id)
    db_item_query = db.query(models.Item).filter_by(
        owner_receiptId = receipt_id,
        id = item_id)
    db_item = db_item_query.first()
    if db_item is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt and Item not found with the given ID")  
    update_data = data_item.dict(exclude_unset=True) 
    db_item_query.filter(models.Item.id == item_id)\
                 .update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.patch("/receipts/editmanyitem/{receipt_id}/{type_receipt}", tags = ["Receipts"])
async def editManyItem(receipt_id: int,
                       type_receipt: int,
                       data_item: List[schemas.EditItem], 
                       db: Session = Depends(get_db)):
    # print(data_item)
    for ele in data_item:
        db_item_query = db.query(models.Item).filter_by(
            owner_receiptId = receipt_id,
            id = ele.id)
        db_item = db_item_query.first()
        if db_item is None :
            print("add!!!!")
            addItem = {}
            if type_receipt == 0:
                addItem = {
                    "nameItem": ele.nameItem,
                    "priceItemTotal": ele.priceItemTotal,
                    "owner_receiptId": receipt_id
                }
            elif type_receipt == 1:
                addItem = {
                    "nameItem": ele.nameItem,
                    "qty": ele.qty,
                    "unitQty": ele.unitQty,
                    "pricePerQty": ele.pricePerQty,
                    "priceItemTotal": ele.priceItemTotal,
                    "owner_receiptId": receipt_id
                }                
            await crud.create_one_item(db, addItem, receipt_id, type_receipt)
        else:
            update_data = ele.dict(exclude_unset=True) 
            db_item_query.filter(models.Item.id == ele.id)\
                         .update(update_data, synchronize_session=False)
            db.commit()
            db.refresh(db_item)
    return {"success": True}

@app.post("/receipts/editonereceipt/{receipt_id}", 
           tags = ["Receipts"], 
           response_model=schemas.ResponseEditReceipt)
async def editOneReceipt(request: Request,
                         receipt_id: int,
                         receiptID: Union[str, None] = Form(...),
                         dateReceipt: Union[str, None] = Form(...),
                         shopName: Union[str, None] = Form(...),
                         shopPhone: Union[str, None] = Form(...),
                         addressShop: Union[str, None] = Form(...),
                         taxIDShop: Union[str, None] = Form(...),
                         customerName: Union[str, None] = Form(...),
                         addressCust: Union[str, None] = Form(...),
                         taxIDCust: Union[str, None] = Form(...),
                         db: Session = Depends(get_db)):
    # print(receiptID)
    db_receipt_query = db.query(models.Receipt).filter_by(id = receipt_id)
    db_receipt = db_receipt_query.first()
    if db_receipt is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt not found with the given ID") 
    update_data = {
        "receiptID": receiptID,
        "dateReceipt": dateReceipt,
        "shopName": shopName,
        "shopPhone": shopPhone,
        "addressShop": addressShop,
        "taxIDShop": taxIDShop,
        "customerName": customerName,
        "addressCust": addressCust,
        "taxIDCust": taxIDCust,
    }
    # print(update_data)
    # update_data = data_receipt.dict(exclude_unset=True)
    db_receipt_query.filter(models.Receipt.id == receipt_id)\
                    .update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_receipt)
    # return db_receipt
    redirect_url = request.url_for('editreceipt', **{"receipt_id": receipt_id})   
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
