from sqlalchemy.orm import Session

from . import models, schemas

def create_receipt(db: Session, data: schemas.ReceiptCreate):
    db_receipt = models.Receipt(receiptID=data.receiptID)
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt

def create_receipt_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
