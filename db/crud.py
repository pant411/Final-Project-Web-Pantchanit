from sqlalchemy.orm import Session
from typing import List, Union
import datetime
from . import models, schemas

#################################### for get method #################################### 

async def create_receipt_main(db: Session, receipt: Union[schemas.ReceiptCreateMain, dict]):
    # create shop
    # print(receipt)

    db_receipt = models.Receipt(
        filename = receipt["filename"],
        pathImage = receipt["pathImage"],
        receiptID = receipt["receiptID"], 
        dateReceipt = receipt["dateReceipt"],
        shopName = receipt["shopName"], 
        taxIDShop = receipt["taxIDShop"], 
        addressShop = receipt["addressShop"],
        shopPhone = receipt["shopPhone"],
        customerName = receipt["customerName"],
        addressCust = receipt["addressCust"],
        taxIDCust = receipt["taxIDCust"],
        type_item = receipt["type_item"],
        status = 1,
        Created_At = datetime.datetime.now(),
        Updated_At = datetime.datetime.now()
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    db_item = await create_item(
            db, 
            listItems = receipt["items"],
            owner_receiptId = db_receipt.id,
            type_item=receipt["type_item"])
    return db_receipt

async def create_item(db: Session, listItems: any, owner_receiptId: int, type_item: int):
    objects = []
    for ele in listItems:
        if type_item == 0:
            db_items = models.Item(
                nameItem = ele["nameItem"], 
                priceItemTotal = ele["priceItemTotal"],
                owner_receiptId = owner_receiptId
            )
        elif type_item == 1:
            db_items = models.Item(
                nameItem = ele["nameItem"], 
                qty = ele["qty"],
                unitQty = ele["unitQty"],
                pricePerQty = ele["pricePerQty"],
                priceItemTotal = ele["priceItemTotal"],
                owner_receiptId = owner_receiptId
            )        
        objects.append(db_items)
    db.bulk_save_objects(objects)
    db.commit()

async def create_one_item(db: Session, item: any, owner_receiptId: int):
    db_item = None
    print(item)
    db_item = models.Item(
            nameItem = item["nameItem"], 
            qty = item["qty"],
            unitQty = item["unitQty"],
            pricePerQty = item["pricePerQty"],
            priceItemTotal = item["priceItemTotal"],
            owner_receiptId = owner_receiptId
        )        
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

#################################### for get method #################################### 

async def getOneReceipt_byDBId_main(db: Session, id: int):
   db_receipt = db.query(models.Receipt).filter(models.Receipt.id == id).first()
   # db_item = await getItem_byDBId(db, owner_receiptId = id)
   # print(db_item)
   return db_receipt

async def getReceiptByAll(db: Session):
    db_receipt_list = db.query(models.Receipt.id,
                          models.Receipt.filename,
                          models.Receipt.pathImage,
                          models.Receipt.receiptID,
                          models.Receipt.dateReceipt,
                          models.Receipt.shopName,
                          models.Receipt.customerName,
                          models.Receipt.Created_At)\
                    .order_by(models.Receipt.Created_At.desc())\
                    .all()
    return db_receipt_list

async def getStatusReceiptByAll(db: Session):
    db_receipt_list = db.query(models.Receipt.id,
                          models.Receipt.filename,
                          models.Receipt.status,
                          models.Receipt.Created_At,
                          models.Receipt.Updated_At)\
                        .order_by(models.Receipt.Created_At.desc())\
                        .all()
    return db_receipt_list

async def getItem_byDBId(db: Session, owner_receiptId: int):
   db_item = db.query(models.Item).filter_by(owner_receiptId = owner_receiptId).all()
   return db_item

async def getOneItem_byDBId(db: Session, owner_receiptId: int, item_id: int):
   db_item = db.query(models.Item).filter_by(
        owner_receiptId = owner_receiptId,
        id = item_id).first()
   return db_item

async def editOneItem_byDBId(db: Session, owner_receiptId: int, item_id: int):
   db_item = db.query(models.Item).filter_by(
        owner_receiptId = owner_receiptId,
        id = item_id).first()
   return db_item

async def getOneReceiptByID(db: Session, id: int):
    return db.query(models.Receipt).filter(models.Receipt.id == id).first()

#################################### for delete method ####################################
async def removeOneReceipt_byIndex(db: Session, id: int):
    db_receipt = db.query(models.Receipt).filter_by(id=id).first()
    db.delete(db_receipt)
    db.commit()

async def removeOneItemByIndex(db: Session, id: int, owner_receiptId: int):
    db_item = db.query(models.Item).filter_by(id=id, owner_receiptId=owner_receiptId).first()
    db.delete(db_item)
    db.commit()
