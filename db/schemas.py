from typing import List, Union
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.schema import Optional

class Item(BaseModel): # back to Receipt
    nameItem: str
    qty: Optional[float]
    pricePerQty: Optional[float]
    priceItemTotal: float
    class Config:
        orm_mode = True

class ReceiptCreateMain(BaseModel):
    # about receipt
    pathImage: str
    receiptID: str
    dateReceipt: Optional[datetime]
    # about shop
    shopName: str
    taxIDShop: Optional[str]
    addressShop: Optional[str]
    shopPhone: Optional[str]
    # about customer
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    # about item
    items: List[Item] = []
    priceTotal: float
    class Config:
        orm_mode = True

class ResponseShop(BaseModel):
    id: int
    shopName: str
    taxIDShop: str
    addressShop: str
    shopPhone: str

class ResponseCustomer(BaseModel):
    id: int
    customerName: str
    taxIDCust: str
    addressCust: str

class ResponsePurchase(BaseModel):
    id: int
    priceTotal: float
    owner_receiptId: int

class ResponseItem(BaseModel):
    id: int
    nameItem: str
    qty: Optional[float]
    pricePerQty: Optional[float]
    priceItemTotal: float
    owner_purchaseId: int
    class Config:
        orm_mode = True

class ResponseGetOneReceipt(BaseModel):
    id: int
    # about receipt
    pathImage: str
    receiptID: str
    dateReceipt: Optional[datetime]
    shopID: int
    shopName: str
    taxIDShop: Optional[str]
    shopPhone: Optional[str]
    addressShop: Optional[str]
    customerID: Optional[str]
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    purchase_id: int
    priceTotal: float
    list_item: List[ResponseItem] = []
    class Config:
        orm_mode = True

class ResponseReceipt(BaseModel):
    id: int
    pathImage: str
    receiptID: str
    dateReceipt: Optional[datetime]
    shopID: int
    customerID: int
    Created_At: datetime
    Updated_At: datetime

class ResponseCreateReceipt(BaseModel):
    status: str

class ResponseAnalyzeReceipt(BaseModel):
    pathImage: str
    receiptID: str
    dateReceipt: datetime
    shopName: str
    shopPhone: str
    taxIDShop: str
    taxIDCust: str
    addressShop: str
    customer: str
    addressCust: str
