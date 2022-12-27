import cv2
import pytesseract
config = '--tessdata-dir tessdata-dir --oem 1 -l tha+eng --psm 6'

def main(image: cv2.Mat):

    text2 = pytesseract.image_to_string(image,config=config,output_type=pytesseract.Output.DICT) 
    return text2['text']