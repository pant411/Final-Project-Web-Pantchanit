from sqlalchemy import  text,\
                        Column,\
                        ForeignKey,\
                        Integer,\
                        String,\
                        DateTime,\
                        TIMESTAMP,\
                        FLOAT
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from .database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True) # PK
    receiptID = Column(String(250), index=True)
    dateReceipt = Column(DateTime, index=True)
    items = relationship("Item", back_populates="owner_receipt") # FK
    shop = relationship("Shop", back_populates="owner_receipt") # FK
    customer = relationship("Customer", back_populates="owner_receipt") # FK
    priceTotal = Column(FLOAT, index=True)
    pathImage = Column(String(250), index=True)
    Created_At = Column(TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Updated_At = Column(TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

class Item(Base): # back to Receipt
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nameItem = Column(String(250), index=True)
    qty = Column(FLOAT, index=True)
    pricePerQty = Column(FLOAT, index=True)
    priceItem = Column(FLOAT, index=True)
    Created_At = Column(TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Updated_At = Column(TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())
    owner_receiptId = Column(Integer, ForeignKey("receipts.id"))
    owner_receipt = relationship("Receipt", back_populates="items")

class Shop(Base): # back to Receipt
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    shopName = Column(String(250), index=True)
    taxIDShop = Column(String(30), index=True)
    shopPhone = Column(String(30), index=True)
    address = relationship("AddressShop", back_populates="owner_shop") # FK
    Created_At = Column(TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Updated_At = Column(TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    owner_receiptId = Column(Integer, ForeignKey("receipts.id"))
    owner_receipt = relationship("Receipt", back_populates="shop")

class AddressShop(Base): # back to Shop
    __tablename__ = "addressShop"

    id = Column(Integer, primary_key=True, index=True)
    addressShop = Column(String(400), index=True) 
    Created_At = Column(TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Updated_At = Column(TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    owner_shopId = Column(Integer, ForeignKey("shops.id"))
    owner_shop = relationship("Shop", back_populates="address")

class Customer(Base): # back to Receipt
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customerName = Column(String(250), index=True)
    # taxIDCust = Column(String(30), index=True)
    address = relationship("AddressCustomer", back_populates="owner_cust") # FK
    Created_At = Column(TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Updated_At = Column(TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    owner_receiptId = Column(Integer, ForeignKey("receipts.id"))
    owner_receipt = relationship("Receipt", back_populates="customer")

class AddressCustomer(Base): # back to Customer
    __tablename__ = "addressCustomer"

    id = Column(Integer, primary_key=True, index=True)
    addressCust = Column(String(400), index=True) 
    Created_At = Column(TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Updated_At = Column(TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    owner_custId = Column(Integer, ForeignKey("customers.id"))
    owner_cust = relationship("Customer", back_populates="address")