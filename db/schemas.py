from typing import List, Union
from datetime import datetime

from pydantic import BaseModel

class Item(BaseModel): # back to Receipt
    nameItem: str
    qty: float
    pricePerQty: float
    priceTotal: float

    class Config:
        orm_mode = True

class Receipt(BaseModel):
    receiptID: str
    dateReceipt: datetime
    items: List[Item] = []

    class Config:
        orm_mode = True

class AddressShop(BaseModel): # back to Shop
    address: str

class Shop(BaseModel):
    shopName: str
    taxID: str
    address: List[AddressShop]

class AddressCustomer(BaseModel): # back to Shop
    address: str

class Customer(BaseModel):
    customerName: str
    # taxID: str
    address: List[AddressCustomer]

class ReceiptCreate(BaseModel):
    receiptID: str
    dateReceipt: datetime
    items: List[Item] = []

class ItemCreate(BaseModel): # back to Receipt
    nameItem: str
    qty: float
    pricePerQty: float
    priceTotal: float
