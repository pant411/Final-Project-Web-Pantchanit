from typing import List, Union
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.schema import Optional

class Item(BaseModel): 
    # id: int
    nameItem: Optional[str]
    qty: Optional[float]
    unitQty: Optional[str]
    pricePerQty: Optional[float]
    priceItemTotal: Optional[float]
    class Config:
        orm_mode = True

class ReceiptCreateMain(BaseModel):
    # about receipt
    filename: Optional[str]
    pathImage: Optional[str]
    receiptID: Optional[str]
    dateReceipt: Optional[datetime]
    # about shop
    shopName: Optional[str]
    taxIDShop: Optional[str]
    addressShop: Optional[str]
    shopPhone: Optional[str]
    # about customer
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    # about item
    items: List[Item] = []
    # priceTotal: float
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
    unitQty: Optional[str]
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
    list_item: List[Item] = []
    class Config:
        orm_mode = True

class ResponseReceiptAll(BaseModel):
    id: int
    filename: str
    pathImage: str
    receiptID: str
    dateReceipt: Optional[datetime]
    shopName: str
    customerName: str
    class Config:
        orm_mode = True

class ResponseCreateReceipt(BaseModel):
    status: str
    class Config:
        orm_mode = True

class ResponseDeleteReceipt(ResponseCreateReceipt):
    pass

class ResponseAnalyzeReceipt(BaseModel):
    filename: Optional[str]
    pathImage: Optional[str]
    receiptID: Optional[str]
    dateReceipt: Optional[datetime]
    shopName: Optional[str]
    shopPhone: Optional[str]
    taxIDShop: Optional[str]
    taxIDCust: Optional[str]
    addressShop: Optional[str]
    customer: Optional[str]
    addressCust: Optional[str]
    list_item: List[Item] = []
    class Config:
        orm_mode = True

class ResponseShopAll(BaseModel):
    id: int
    shopName: str
    taxIDShop: Optional[str]
    shopPhone: Optional[str]
    addressShop: Optional[str]
    class Config:
        orm_mode = True

class ResponseCustomerAll(BaseModel):
    id: int
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    class Config:
        orm_mode = True
