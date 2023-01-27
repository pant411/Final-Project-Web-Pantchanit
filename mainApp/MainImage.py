import cv2 
import ImageModule as mdl
from deskew import determine_skew

def PreProcess(image: cv2.Mat):
    # image = cv2.imread(img)
    angle = determine_skew(image)
    rotated = mdl.rotate(image, angle, (255, 255, 255))
    removeShadow1 = mdl.removeShadow(rotated)
    adj_img = mdl.adjust_gamma(removeShadow1,0.548)
    remove_bg = mdl.removeBackground(adj_img)
    removeline = mdl.removeLine(remove_bg)
    return removeline
