from pythainlp.util import normalize
from ExtractionModule import findShopName, findPhoneShop, findTaxIDShop, findDate, findReceiptID, findCustomerShop
# from pythainlp.tokenize import sent_tokenize
from Utils import candidateFromList

def extraction(text: str):
    Lines = text.splitlines()
    # list of word may be in an entity
    listShopName = []
    listShopPhone = []
    listShopTaxID = []
    listDate = []
    listReceiptID = []
    listCustomerShop = []
    # text may be a item of goods
    # item_txt = []
    len_line = len(Lines)
    for idx in range(len_line):
        norm_txt = normalize(Lines[idx].strip('\"#$%&()*+:;<=>@[\]^_`{|}~\n'))
        
        if (idx+1)/len_line <= 0.40 or (idx+1)/len_line >= 0.68:
            shopName = findShopName(text = norm_txt, threshold = 0.78)
            if len(shopName) > 8:
                listShopName.append({'lineNum': idx,'shopName': shopName})

            TaxIDShop = findTaxIDShop(text = norm_txt, threshold = 0.72)
            if len(TaxIDShop) >= 13:
                listShopTaxID.append({'lineNum': idx,'TaxIDShop': TaxIDShop})

            shopPhone = findPhoneShop(text = norm_txt, threshold = 0.75)
            if len(shopPhone) > 3 and shopPhone not in TaxIDShop:
                listShopPhone.append({'lineNum': idx,'shopPhone': shopPhone})
            
            DateShop = findDate(text = norm_txt, threshold = 0.72)
            if len(DateShop) > 3:
                listDate.append({'lineNum': idx,'DateShop': DateShop})

            CustomerShop = findCustomerShop(text = norm_txt, threshold = 0.72)
            if len(CustomerShop) > 3:
                listCustomerShop.append({'lineNum': idx,'CustomerShop': CustomerShop})
            
        if (idx+1)/len_line >= 0.1 and (idx+1)/len_line <= 0.35:
            ReceiptID = findReceiptID(text = norm_txt, threshold = 0.75)
            if len(ReceiptID) > 1:
                listReceiptID.append({'lineNum': idx,'ReceiptID': ReceiptID})
        
        # if (idx+1)/len_line > 0.35 and (idx+1)/len_line < 0.68:
        #     item_txt.append(norm_txt)

    shopName = candidateFromList(lst=listShopName,key='shopName')
    # print(f'shopName is {shopName}')

    shopPhone = ''
    if len(listShopPhone) != 0:
        shopPhone = listShopPhone[0]['shopPhone']
    # print(f'shopPhone is {shopPhone}')

    taxIDShop = ''
    if len(listShopTaxID) != 0:
        taxIDShop = listShopTaxID[0]['TaxIDShop']
    # print(f'taxIDShop is {taxIDShop}')

    dateReceipt = ''
    if len(listDate) != 0:
        dateReceipt = listDate[0]['DateShop']
    # print(f'dateReceipt is {dateReceipt}')

    receiptID = ''
    if len(listReceiptID) != 0:
        receiptID = listReceiptID[0]['ReceiptID']

    ''' return { 'shopName':shopName, 
             'shopPhone':shopPhone, 
             'taxIDShop':taxIDShop, 
             'dateReceipt':dateReceipt, 
             'receiptID':receiptID
        }
    '''
    return shopName,shopPhone,taxIDShop,dateReceipt,receiptID