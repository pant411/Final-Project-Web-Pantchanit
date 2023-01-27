import sys
sys.path.append("EntityExtraction")
sys.path.append("ImgPreprocess")
from EntityExtraction import mainApp
from ImgPreprocess import PreProcess
# import cv2
import pytesseract
config = '--tessdata-dir tessdata-dir --oem 1 -l tha+eng --psm 6'

def runMain(image_file):
    pre_img = PreProcess(image_file)
    ocr_res = pytesseract.image_to_string(pre_img,config=config) 
    shopName,shopPhone,taxIDShop,dateReceipt,receiptID = mainApp(ocr_res)
    return shopName,shopPhone,taxIDShop,dateReceipt,receiptID

# x = runMain('Receipts_ImgPreprocess/Resource/receipt/20220916_072744059_iOS.jpg')
# print(x)