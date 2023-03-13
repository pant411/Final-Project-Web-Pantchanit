# built in module
from typing import Union, List
from fastapi import FastAPI, Request, File, UploadFile, status, Depends, HTTPException, Response, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
# from werkzeug.utils import secure_filename
from ExtractionFromImageService import main_service
from fastapi.concurrency import run_in_threadpool

from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

from google.cloud import storage
import os
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime, timedelta
import re

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

app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")

templates = Jinja2Templates(directory="templates")

# define function that generates the public URL, default expiration is set to 24 hours
def get_cs_file_url(bucket_name, file_name, expire_in=datetime.now() + timedelta(5000)): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    url = bucket.blob(file_name).generate_signed_url(expire_in)

    return url

def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    # print(
    #     f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
    # )
    return True
        
#################################### Template Module #################################### 

@app.get("/home", response_class=HTMLResponse)
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
    return templates.TemplateResponse("receiptdetail.html", {
        "request": request, 
        "receipt_data": receipt_data, 
        "items": db_item})

@app.get("/", response_class=HTMLResponse)
async def getlistReceiptAllPage(request: Request, db: Session = Depends(get_db)):
    list_data = await crud.getReceiptByAll(db)
    return templates.TemplateResponse("listReceipt.html", {
        "request": request, 
        "list_data": list_data})

@app.get("/statusreceipts", response_class=HTMLResponse)
async def getStatusReceipt(request: Request, db: Session = Depends(get_db)):
    list_data = await crud.getStatusReceiptByAll(db)
    # list_data = []
    return templates.TemplateResponse("statusReceipt.html", {
        "request": request, 
        "list_data": list_data
    })

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
                        file: UploadFile = File(...), 
                        db: Session = Depends(get_db)):
    content_receipt = file.file.read()           
    data = main_service(content_receipt)
    upload_blob_from_memory(os.getenv("BUCKETNAME_STORAGE"),content_receipt, file.filename)
    data["pathImage"] = get_cs_file_url(os.getenv("BUCKETNAME_STORAGE"),file.filename)
    data["filename"] = file.filename
    
    db_receipt = await crud.create_receipt_main(db=db, 
                                                receipt=data)    
    redirect_url = request.url_for('editreceipt', **{"receipt_id": db_receipt.id})   
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/receipts/submitmultiple", tags = ["Receipts"])
async def submitMultipleReceipt(files: List[UploadFile] = File(...),
                                db: Session = Depends(get_db)):
    if len(files) > 10:
        raise HTTPException(status_code=404, 
                            detail="You can upload a maximum of 10 images.")  
    for idx in range(len(files)):
        if re.search("^.*\.(jpg|jpeg|png|tiff|tif|bmp)$",files[idx].filename):
            content_receipt = files[idx].file.read()
            data = main_service(content_receipt)
            upload_blob_from_memory(
                os.getenv("BUCKETNAME_STORAGE"),
                content_receipt, 
                files[idx].filename)
            data["pathImage"] = get_cs_file_url(
                os.getenv("BUCKETNAME_STORAGE"), 
                files[idx].filename)
            data["filename"] = files[idx].filename
            db_receipts = await crud.create_receipt_main(db, data)
    return RedirectResponse("/statusreceipts", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/receipts/getOneByID/{receipt_id}", 
         tags = ["Receipts"], 
         response_model=schemas.ResponseGetOneReceipt)
async def getOneReceipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = crud.getOneReceiptByID(db, id = receipt_id)
    if db_receipt is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt not found with the given ID")
    return await crud.getOneReceipt_byDBId_main(db, receipt_id)

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

@app.get("/receipts/getlistreceipts", response_model=schemas.ResponseReceiptAll, tags = ["Receipts"])
async def getAllReceiptList(db: Session = Depends(get_db)):
    return await crud.getReceiptByAll(db)

@app.get("/receipts/getstatusreceipts", response_model=schemas.ResponseStatusReceiptAll, tags = ["Receipts"])
async def getStatusReceiptList(db: Session = Depends(get_db)):
    return await crud.getStatusReceiptByAll(db)

@app.get("/receipts/getlistreceiptpagination", response_model=Page[schemas.ResponseReceiptAll], tags = ["Receipts"])
async def getAllReceiptPagination(db: Session = Depends(get_db)):
    list_data = await crud.getReceiptByAll(db)
    return paginate(list_data)

@app.get("/receipts/statusreceiptspagination", response_model=Page[schemas.ResponseStatusReceiptAll], tags = ["Receipts"])
async def getStatusReceiptPagination(db: Session = Depends(get_db)):
    list_data = await crud.getStatusReceiptByAll(db)
    return paginate(list_data)

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

@app.post("/receipts/editonereceipt/{receipt_id}", 
           tags = ["Receipts"], 
           response_model=schemas.ResponseEditReceipt)
async def editOneReceipt(request: Request,
                         receipt_id: int,
                         receiptID: Union[str, None] = Form(default=None),
                         dateReceipt: Union[str, None] = Form(default=None),
                         shopName: Union[str, None] = Form(default=None),
                         shopPhone: Union[str, None] = Form(default=None),
                         addressShop: Union[str, None] = Form(default=None),
                         taxIDShop: Union[str, None] = Form(default=None),
                         customerName: Union[str, None] = Form(default=None),
                         addressCust: Union[str, None] = Form(default=None),
                         taxIDCust: Union[str, None] = Form(default=None),
                         db: Session = Depends(get_db)):
    print(receiptID)
    db_receipt_query = db.query(models.Receipt).filter_by(id = receipt_id)
    db_receipt = db_receipt_query.first()
    if db_receipt is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt not found with the given ID") 
    
    update_data = {}
    if receiptID: update_data["receiptID"] = receiptID
    if dateReceipt: update_data["dateReceipt"] = dateReceipt
    if shopName: update_data["shopName"] = shopName
    if shopPhone: update_data["shopPhone"] = shopPhone
    if addressShop: update_data["addressShop"] = addressShop
    if taxIDShop: update_data["taxIDShop"] = taxIDShop
    if customerName: update_data["customerName"] = customerName
    if addressCust: update_data["addressCust"] = addressCust
    if taxIDCust: update_data["taxIDCust"] = taxIDCust

    # print(update_data)
    # update_data = data_receipt.dict(exclude_unset=True)
    db_receipt_query.filter(models.Receipt.id == receipt_id)\
                    .update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_receipt)
    # return db_receipt
    redirect_url = request.url_for('editreceipt', **{"receipt_id": receipt_id})   
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

@app.patch("/receipts/editreceiptall/{receipt_id}/{type_item}", tags = ["Receipts"])
async def editReceiptAll(receipt_id: int,
                         type_item: int,
                         payload: schemas.SubmitEditItem, 
                         db: Session = Depends(get_db)):
    # print(payload)
    db_receipt_query = db.query(models.Receipt).filter_by(id = receipt_id)
    db_receipt = db_receipt_query.first()
    if db_receipt is None:
        raise HTTPException(status_code=404, 
                            detail="Receipt not found with the given ID") 
    update_data = (payload.dataReceipt).dict(exclude_unset=True)
    update_data["status"] = 2
    update_data["Updated_At"] = datetime.now()
    db_receipt_query.filter(models.Receipt.id == receipt_id)\
                    .update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_receipt)

    for ele in payload.editItem:
        db_item_query = db.query(models.Item).filter_by(
            owner_receiptId = receipt_id,
            id = ele.id)
        db_item = db_item_query.first()
        if db_item is None :
            addItem = {}
            if type_item == 0:
                addItem = {
                    "nameItem": ele.nameItem,
                    "priceItemTotal": ele.priceItemTotal,
                    "owner_receiptId": receipt_id
                }
            elif type_item == 1:
                addItem = {
                    "nameItem": ele.nameItem,
                    "qty": ele.qty,
                    "unitQty": ele.unitQty,
                    "pricePerQty": ele.pricePerQty,
                    "priceItemTotal": ele.priceItemTotal,
                    "owner_receiptId": receipt_id
                }           
            await crud.create_one_item(db, addItem, receipt_id)
        else:
            update_data = ele.dict(exclude_unset=True) 
            if type_item == 0:
                update_data["qty"] = None
                update_data["unitQty"] = None
                update_data["pricePerQty"] = None
            db_item_query.filter(models.Item.id == ele.id)\
                         .update(update_data, synchronize_session=False)
            db.commit()
            db.refresh(db_item)

    for ele in payload.deleteItem:
        await crud.removeOneItemByIndex(db, id = ele, owner_receiptId=receipt_id)
    
    return {"success": True}
    # redirect_url = request.url_for('receiptdetail', **{"receipt_id": receipt_id})   
    # return RedirectResponse(redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

