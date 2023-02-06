from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True) # PK
    receiptID = Column(String, index=True)
    dateReceipt = Column(DateTime, index=True)
    items = relationship("Item", back_populates="owner_receipt") # FK
    shop = relationship("Item", back_populates="owner_receipt") # FK
    customer = relationship("Item", back_populates="owner_receipt") # FK
    priceTotal = Column(Integer, index=True)
    Created_At = Column(TIMESTAMP, index=True)
    Updated_At = Column(TIMESTAMP, index=True)

class Item(Base): # back to Receipt
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nameItem = Column(String, index=True)
    qty = Column(Integer, index=True)
    pricePerQty = Column(Integer, index=True)
    priceTotal = Column(Integer, index=True)
    Created_At = Column(TIMESTAMP, index=True)
    Updated_At = Column(TIMESTAMP, index=True)

    owner_receiptId = Column(Integer, ForeignKey("receipts.id"))
    owner_receipt = relationship("Receipt", back_populates="items")

class Shop(Base): # back to Receipt
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    shopName = Column(String, index=True)
    taxID = Column(String, index=True)
    address = relationship("AddressShop", back_populates="owner_shop") # FK
    Created_At = Column(TIMESTAMP, index=True)
    Updated_At = Column(TIMESTAMP, index=True)

    owner_receiptId = Column(Integer, ForeignKey("receipts.id"))
    owner_receipt = relationship("Receipt", back_populates="shop")

class AddressShop(Base): # back to Shop
    __tablename__ = "addressShop"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True) 
    Created_At = Column(TIMESTAMP, index=True)
    Updated_At = Column(TIMESTAMP, index=True)

    owner_shopId = Column(Integer, ForeignKey("shops.id"))
    owner_shop = relationship("Shop", back_populates="address")

class Customer(Base): # back to Receipt
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customerName = Column(String, index=True)
    # taxID = Column(String, index=True)
    address = relationship("AddressCustomer", back_populates="owner_cust") # FK
    Created_At = Column(TIMESTAMP, index=True)
    Updated_At = Column(TIMESTAMP, index=True)

    owner_receiptId = Column(Integer, ForeignKey("receipts.id"))
    owner_receipt = relationship("Receipt", back_populates="customer")

class AddressCustomer(Base): # back to Customer
    __tablename__ = "addressCustomer"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True) 
    Created_At = Column(TIMESTAMP, index=True)
    Updated_At = Column(TIMESTAMP, index=True)

    owner_custId = Column(Integer, ForeignKey("customers.id"))
    owner_cust = relationship("Customer", back_populates="address")