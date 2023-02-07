from sqlalchemy.orm import Session
from typing import List

from . import models, schemas

def create_receipt_main(db: Session, receipt: schemas.ReceiptCreateMain):
    db_receipt = models.Receipt(
        receiptID = receipt.receiptID, 
        pathImage = receipt.pathImage,
        dateReceipt = receipt.dateReceipt,
        priceTotal = receipt.priceTotal
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    print(db_receipt.id)

    db_shop = create_shop(db, receipt.shopName, receipt.taxIDShop, receipt.addressShop, db_receipt.id)

    db_cust = create_customer(db, receipt.customerName, receipt.addressCust, db_receipt.id)

    create_item(db, receipt.items, db_receipt.id)

    return {"status": "success"}

def create_shop(db: Session, shopName: str, taxIDShop: str, addressShop: str, owner_receiptId: int):
    db_shop = models.Shop(
        shopName = shopName, 
        taxIDShop = taxIDShop,
        owner_receiptId = owner_receiptId
    )
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)

    db_addr_shop = create_shopAddress(db, addressShop, db_shop.id)

    return db_shop

def create_shopAddress(db: Session, addressShop: str, owner_shopId: int):
    db_addr_shop = models.AddressShop(
        addressShop = addressShop, 
        owner_shopId = owner_shopId
    )
    db.add(db_addr_shop)
    db.commit()
    db.refresh(db_addr_shop)
    return db_addr_shop

def create_customer(db: Session, customerName: str, addressCust: str, owner_receiptId: int):
    db_cust = models.Customer(
        customerName = customerName, 
        # taxIDCustomer = receipt.taxIDCustomer,
        owner_receiptId = owner_receiptId
    )
    db.add(db_cust)
    db.commit()
    db.refresh(db_cust)

    db_addr_cust = create_customerAddress(db, addressCust, db_cust.id)
    db.refresh(db_addr_cust)

    return db_cust

def create_customerAddress(db: Session, addressCust: str, owner_custId: int):
    db_addr_cust = models.AddressCustomer(
        addressCust = addressCust, 
        owner_custId = owner_custId
    )
    db.add(db_addr_cust)
    db.commit()
    db.refresh(db_addr_cust)
    return db_addr_cust

def create_item(db, listItems: any, owner_receiptId: int):
    for ele in listItems:
        db_items = models.Item(
            nameItem = ele.nameItem, 
            qty = ele.qty,
            pricePerQty = ele.pricePerQty,
            priceItem = ele.priceItem,
            owner_receiptId = owner_receiptId
        )
        db.add(db_items)
        db.commit()
        db.refresh(db_items)    
