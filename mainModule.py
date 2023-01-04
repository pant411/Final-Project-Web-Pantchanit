from Receipts_EntityExtraction.main import mainApp
from Receipts_ImgPreprocess.preprocess import PreProcess
from TesseractModule.RunTesseract import mainTesseract
import cv2

def runMain(image_file):
    image = cv2.imread(image_file)
    pre_img = PreProcess(image)
    ocr_res =  mainTesseract(pre_img)
    print(ocr_res)
    extract_res = mainApp(ocr_res)
    return extract_res 

print(runMain('/Receipts_ImgPreprocess/Resource/receipt/20220916_072744059_iOS.jpg'))