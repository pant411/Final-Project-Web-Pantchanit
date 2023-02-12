from sqlalchemy import  text,\
                        Column,\
                        ForeignKey,\
                        Integer,\
                        String,\
                        DateTime,\
                        TIMESTAMP,\
                        FLOAT,\
                        func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from .database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True) # PK
    filename = Column(String(250), index=True)
    pathImage = Column(String(250), index=True)
    receiptID = Column(String(250), index=True)
    dateReceipt = Column(DateTime, index=True)
    purchase = relationship("Purchase", back_populates="owner_receipt", cascade="all, delete") # FK
    shopID = Column(Integer, index=True)
    customerID =Column(Integer, index=True)
    
    Created_At = Column(TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Updated_At = Column(TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())
    
class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    items = relationship("Item", back_populates="owner_purchase", cascade="all, delete") # FK
    priceTotal = Column(FLOAT, index=True)

    owner_receiptId = Column(Integer, ForeignKey("receipts.id"))
    owner_receipt = relationship("Receipt", back_populates="purchase", cascade="all, delete")

class Item(Base): # back to Receipt
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nameItem = Column(String(250), index=True)
    qty = Column(FLOAT, index=True)
    unitQty = Column(String(10), index=True)
    pricePerQty = Column(FLOAT, index=True)
    priceItemTotal = Column(FLOAT, index=True)

    owner_purchaseId = Column(Integer, ForeignKey("purchases.id"))
    owner_purchase = relationship("Purchase", back_populates="items", cascade="all, delete")

class Shop(Base): # back to Receipt
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    shopName = Column(String(250), index=True)
    taxIDShop = Column(String(30), index=True)
    shopPhone = Column(String(30), index=True)
    addressShop = Column(String(250), index=True)

class Customer(Base): # back to Receipt
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customerName = Column(String(250), index=True)
    taxIDCust = Column(String(30), index=True)
    addressCust = Column(String(250), index=True)
    