from pythainlp.util import normalize
from ExtractionModule import findShopName,\
                             findPhoneShop,\
                             findTaxIDShop,\
                             findDate,\
                             findReceiptID,\
                             findCustomerShop,\
                             extractAddress,\
                             findListOfItemWithQty,\
                             findListOfItemWithoutQty\
#                              findListOfItemWithoutQty
# from pythainlp.tokenize import sent_tokenize
# import json
from Utils import candidateFromList, normalizeDate
import re

def extraction(text: str, option: int):
    Lines = text.splitlines()

    item_txt1 = []
    item_txt2 = []
    item_txt_total = []

    len_line = len(Lines)
    line_item_txt1_p1 = ()
    line_item_txt1_p2 = ()

    for idx in range(len_line):
        norm_txt = normalize(Lines[idx])
        norm_txt = re.sub(r'[\"#$%&()*+:;<=>@[\]^_`{|}~\n]', '', norm_txt)
        norm_txt = re.sub(r'^\s', '', norm_txt)
        if (idx+1)/len_line <= 0.45 or (idx+1)/len_line >= 0.68:
            item_txt1.append({"line-num": idx,"txt": norm_txt})
            line_item_txt1_p1 = (0,int(0.45*len_line)-1)
            line_item_txt1_p2 = (int(0.68*len_line),len_line-1)
        if (idx+1)/len_line > 0.25:
            item_txt2.append({"line-num": idx,"txt": norm_txt})
        # item_txt_total.append({"line-num": idx,"txt": norm_txt})    
 

    listAddress = extractAddress(
                lsttext = item_txt1,
                line_item_txt1_p1=line_item_txt1_p1,
                line_item_txt1_p2=line_item_txt1_p2
            )
    
    listShopName = findShopName(
                lsttext = item_txt1, 
                threshold = 0.78,
                line_item_txt1_p1=line_item_txt1_p1, 
                finish_line_p1=listAddress['line-addr-shop']
            )

    listShopTaxID = findTaxIDShop(lsttext = item_txt1, threshold = 0.76)

    listShopPhone = findPhoneShop(
                lsttext = item_txt1,
                listShopTaxID = listShopTaxID
            )
    
    listDate = findDate(lsttext = item_txt1, threshold = 0.75)

    listReceiptID = findReceiptID(lsttext = item_txt1, threshold = 0.75)

    listCustomerShop = findCustomerShop(
                    lsttext = item_txt1, 
                    line_end = listAddress["line-addr-customer"], 
                    threshold = 0.72
                )
    
    listOfItem = []

    if option == 0:
        listOfItem = findListOfItemWithoutQty(lsttext = item_txt2)
    elif option == 1:
        listOfItem = findListOfItemWithQty(lsttext = item_txt2)

    # listListOfItem = findListOfItem(lsttext = item_txt2, threshold = 0.80)

    receiptID = ''
    if len(listReceiptID) != 0:
        receiptID = listReceiptID[0] 

    dateReceipt = None
    if len(listDate) != 0:
        # print(listDate)
        dateReceipt = normalizeDate(listDate[0]) 

    shopName = ''
    if len(listShopName) != 0:
        shopName = candidateFromList(lst=listShopName)

    shopPhone = ''
    if len(listShopPhone) != 0:
        shopPhone = listShopPhone[0]

    taxIDShop = ''
    taxIDCust = ''
    if len(listShopTaxID) >= 2:
        taxIDShop = listShopTaxID[0]
        taxIDCust = listShopTaxID[1]
    elif len(listShopTaxID) == 1:
        taxIDShop = listShopTaxID[0]

    customerName = ''
    if len(listCustomerShop) != 0:
        customerName = listCustomerShop[0]

    return { 'shopName': shopName, 
             'shopPhone': shopPhone, 
             'taxIDShop': taxIDShop, 
             'dateReceipt': dateReceipt, 
             'receiptID': receiptID,
             'customerName': customerName,
             'taxIDCust': taxIDCust,
             'addressShop': listAddress["addressShop"],
             'addressCust': listAddress["addressCust"],
             'items': listOfItem
        }
