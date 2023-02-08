from sqlalchemy.orm import Session
from typing import List

from . import models, schemas

#################################### for get method #################################### 

def create_receipt_main(db: Session, receipt: schemas.ReceiptCreateMain):
    # create shop
    db_shop = create_shop(
                db, 
                shopName = receipt.shopName, 
                taxIDShop = receipt.taxIDShop, 
                addressShop = receipt.addressShop,
                shopPhone = receipt.shopPhone)
    # create customer
    db_cust = create_customer(db,
                customerName = receipt.customerName,
                addressCust = receipt.addressCust,
                taxIDCust = receipt.taxIDCust)

    db_receipt = models.Receipt(
        pathImage = receipt.pathImage,
        receiptID = receipt.receiptID, 
        dateReceipt = receipt.dateReceipt,
        shopID = db_shop.id,
        customerID = db_cust.id
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)

    create_purchase(db, listItems = receipt.items, priceTotal = receipt.priceTotal, owner_receiptId = db_receipt.id)

    return {"status": "success"}

def create_shop(db: Session, 
                shopName: str, 
                taxIDShop: str, 
                addressShop: str,
                shopPhone: str):
    db_shop = getOneShopName_byValue(db, 
                                     shopName = shopName,
                                     taxIDShop = taxIDShop,
                                     addressShop = addressShop,
                                     shopPhone = shopPhone)
    if db_shop is None:
        db_shop = models.Shop(
            shopName = shopName, 
            taxIDShop = taxIDShop,
            addressShop = addressShop,
            shopPhone = shopPhone
        )
        db.add(db_shop)
        db.commit()
        db.refresh(db_shop)
    return db_shop

def create_customer(db: Session, 
                    customerName: str, 
                    addressCust: str,
                    taxIDCust: str):
    db_cust = getOneCustomerName_byValue(db, 
                                         customerName = customerName, 
                                         addressCust = addressCust, 
                                         taxIDCust = taxIDCust)
    if db_cust is None:
        db_cust = models.Customer(
            customerName = customerName, 
            taxIDCust = taxIDCust,
            addressCust = addressCust)
        db.add(db_cust)
        db.commit()
        db.refresh(db_cust)

    return db_cust

def create_purchase(db: Session, listItems: any, priceTotal: int, owner_receiptId: int):
    db_purchase = models.Purchase(
        priceTotal = priceTotal,
        owner_receiptId = owner_receiptId
    )
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)

    create_item(db, listItems = listItems, owner_purchaseId = db_purchase.id)

def create_item(db: Session, listItems: any, owner_purchaseId: int):
    objects = []
    for ele in listItems:
        db_items = models.Item(
            nameItem = ele.nameItem, 
            qty = ele.qty,
            pricePerQty = ele.pricePerQty,
            priceItemTotal = ele.priceItemTotal,
            owner_purchaseId = owner_purchaseId
        )
        objects.append(db_items)
    db.bulk_save_objects(objects)
    db.commit()

#################################### for get method #################################### 

def getOneShopName_byValue(db: Session, 
                           shopName: str, 
                           taxIDShop: str, 
                           addressShop: str,
                           shopPhone: str):
    return db.query(models.Shop)\
             .filter(models.Shop.shopName == shopName,
                     models.Shop.taxIDShop == taxIDShop ,
                     models.Shop.addressShop == addressShop,
                     models.Shop.shopPhone == shopPhone)\
             .first()

def getOneCustomerName_byValue(db: Session,
                               customerName: str, 
                               addressCust: str, 
                               taxIDCust: str):
    return db.query(models.Customer)\
             .filter(models.Customer.customerName == customerName,
                     models.Customer.addressCust == addressCust,
                     models.Customer.taxIDCust == taxIDCust)\
             .first()

def getOneReceipt_byDBId_main(db: Session, id: int):
   db_receipt = db.query(models.Receipt).filter(models.Receipt.id == id).first()
   db_shop = getOneShop_byDBId(db, id = db_receipt.shopID)
   db_customer = getOneCustomer_byDBId(db, id = db_receipt.customerID)
   db_purchase = getOnePurchase_byDBId(db, id = db_receipt.id)
   db_item = getItem_byDBId(db, id = db_purchase.id)
   return {
        'id': db_receipt.id,
        'pathImage': db_receipt.pathImage,
        'receiptID': db_receipt.receiptID,
        'dateReceipt': db_receipt.dateReceipt,
        'shopID': db_shop.id,
        'shopName': db_shop.shopName,
        'taxIDShop': db_shop.taxIDShop,
        'shopPhone': db_shop.shopPhone,
        'addressShop': db_shop.addressShop,
        'customerID': db_customer.id,
        'customerName': db_customer.customerName,
        'taxIDCust': db_customer.taxIDCust,
        'addressCust': db_customer.addressCust,
        'purchase_id': db_purchase.id,
        'priceTotal': db_purchase.priceTotal,
        'list_item': db_item
   }

def getReceiptByAll(db: Session):
    db_receipt = db.query(models.Receipt.id,
                          models.Receipt.pathImage,
                          models.Receipt.receiptID,
                          models.Receipt.dateReceipt,
                          models.Shop.shopName,
                          models.Customer.customerName)\
                   .join(models.Customer, models.Receipt.customerID==models.Customer.id)\
                   .join(models.Shop, models.Receipt.shopID==models.Shop.id)\
                   .all()
    return db_receipt

def getOneShop_byDBId(db: Session, id: int):
   db_shop = db.query(models.Shop).filter(models.Shop.id == id).first()
   return db_shop

def getOneCustomer_byDBId(db: Session, id: int):
   db_customer = db.query(models.Customer).filter(models.Customer.id == id).first()
   return db_customer

def getOnePurchase_byDBId(db: Session, id: int):
   db_purchase = db.query(models.Purchase).filter(models.Purchase.owner_receiptId == id).first()
   return db_purchase

def getItem_byDBId(db: Session, id: int):
   db_item = db.query(models.Item).filter(models.Item.owner_purchaseId == id).all()
   return db_item

def getShopAll(db: Session):
    db_shop = db.query(models.Shop).all()
    return db_shop

def getCustomerAll(db: Session):
    db_cust = db.query(models.Customer).all()
    return db_cust

def getOneReceiptByID(db: Session, id: int):
    return db.query(models.Receipt).filter(models.Receipt.id == id).first()

#################################### for delete method ####################################
def removeOneReceipt_byIndex(db: Session, id: int):
    db_receipt = db.query(models.Receipt).filter_by(id=id).first()
    db.delete(db_receipt)
    db.commit()

#################################### for patch method ####################################
# def editOneReceipt_byIndex():
#    return None
