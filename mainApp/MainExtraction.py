from pythainlp.util import normalize
from ExtractionModule import findShopName, findPhoneShop,\
    findTaxIDShop,findDate, findReceiptID, findCustomerShop,\
    findListOfItem, extractAddress
from Utils import candidateFromList

def extraction(text: str):
    Lines = text.splitlines()

    item_txt1 = []
    item_txt2 = []

    len_line = len(Lines)
    line_item_txt1_p1 = ()
    line_item_txt1_p2 = ()

    for idx in range(len_line):
        norm_txt = normalize(Lines[idx].strip('\"#$%&()*+:;<=>@[\]^_`{|}~\n'))
        if (idx+1)/len_line <= 0.45 or (idx+1)/len_line >= 0.68:
            item_txt1.append({"line-num": idx,"txt": norm_txt})
            line_item_txt1_p1 = (0,int(0.45*len_line)-1)
            line_item_txt1_p2 = (int(0.68*len_line),len_line-1)
        if (idx+1)/len_line > 0.2 and (idx+1)/len_line <= 0.68:
            item_txt2.append({"line-num": idx,"txt": norm_txt})    

    listAddress = extractAddress(lsttext = item_txt1,line_item_txt1_p1=line_item_txt1_p1,line_item_txt1_p2=line_item_txt1_p2)
    listShopTaxID = findTaxIDShop(lsttext = item_txt1, threshold = 0.72)
    listShopPhone = findPhoneShop(lsttext = item_txt1,listShopTaxID = listShopTaxID)
    listDate = findDate(lsttext = item_txt1, threshold = 0.72)
    listReceiptID = findReceiptID(lsttext = item_txt1, threshold = 0.75)
    listShopName = findShopName(lsttext = item_txt1, threshold = 0.78)
    listCustomerShop = findCustomerShop(lsttext = item_txt1, line_end = listAddress["line-addr-customer"], threshold = 0.72)
    listListOfItem = findListOfItem(lsttext = item_txt2, threshold = 0.80)

    shopName = candidateFromList(lst=listShopName)

    shopPhone = ''
    if len(listShopPhone) != 0:
        shopPhone = listShopPhone[0]

    taxIDShop = ''
    if len(listShopTaxID) != 0:
        taxIDShop = listShopTaxID[0]

    dateReceipt = ''
    if len(listDate) != 0:
        dateReceipt = listDate[0]

    receiptID = ''
    if len(listReceiptID) != 0:
        receiptID = listReceiptID[0]

    customer = ''
    if len(listCustomerShop) != 0:
        customer = listCustomerShop[0]

    return { 'shopName': shopName, 
             'shopPhone': shopPhone, 
             'taxIDShop': taxIDShop, 
             'dateReceipt': dateReceipt, 
             'receiptID': receiptID,
             'customer': customer,
             'address-shop': listAddress["addr-shop"],
             'address-customer': listAddress["addr-customer"]
        }