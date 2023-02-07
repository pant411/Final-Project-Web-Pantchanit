from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.schema import Optional

class Item(BaseModel): # back to Receipt
    nameItem: str
    qty: Optional[float]
    pricePerQty: Optional[float]
    priceItem: float
    class Config:
        orm_mode = True

class ReceiptCreateMain(BaseModel):
    # about receipt
    pathImage: str
    receiptID: str
    dateReceipt: datetime
    # about shop
    shopName: str
    taxIDShop: str
    addressShop: str
    # about customer
    customerName: str
    # taxIDCust: str
    addressCust: str
    # about item
    items: List[Item] = []
    priceTotal: float

class ShopCreate(BaseModel):
    shopName: str
    taxIDShop: str
    addressShop: str
    owner_receiptId: int

class ShopAddressCreate(BaseModel):
    addressShop: str
    owner_shopId: int

class CustomerCreate(BaseModel): # back to Receipt
    customerName: str
    # taxIDCustomer: str
    addressCust: str
    owner_receiptId: int

class CustomerAddressCreate(BaseModel):
    addressCust: str
    owner_custId: int

class ItemCreate(BaseModel): # back to Receipt
    nameItem: str
    qty: Optional[float]
    pricePerQty: Optional[float]
    priceItem: float
    owner_receiptId: int

class ResponseCreateReceipt(BaseModel):
    status: str