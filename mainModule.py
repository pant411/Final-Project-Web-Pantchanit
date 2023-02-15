import sys
sys.path.append("mainApp")
from mainApp.MainExtraction import extraction
from mainApp.MainImage import PreProcess
# import cv2
import pytesseract
config = '--tessdata-dir tessdata-dir --oem 1 -l tha+eng --psm 6'

def runMain(image_file, option: int):
    # option is 0 (without Qty)
    # option is 1 (with Qty)
    pre_img = PreProcess(image_file)
    ocr_res = pytesseract.image_to_string(pre_img,config=config) 
    res = extraction(ocr_res, option)
    return res

# x = runMain('Receipts_ImgPreprocess/Resource/receipt/20220916_072744059_iOS.jpg')
# print(x)