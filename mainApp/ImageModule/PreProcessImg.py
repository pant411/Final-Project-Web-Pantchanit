import cv2 
import numpy as np
import math
import matplotlib.pyplot as plt

def removeShadow(img: cv2.Mat):
    rgb_planes = cv2.split(img)
    type_rgb_plane = rgb_planes[0].dtype
    result_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((29,29), type_rgb_plane))
        # display_image(dilated_img)
        # bg_img = cv2.medianBlur(dilated_img, 141)
        bg_img = cv2.GaussianBlur(dilated_img, (227, 227), 0)
        # display_image(bg_img)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        # display_image(diff_img)
        result_planes.append(diff_img)
    return cv2.merge(result_planes)

def removeBackground(myimage: cv2.Mat):
    # Blur to image to reduce noise
    # myimage = cv2.GaussianBlur(myimage,(1,1), 0)
    myimage = cv2.medianBlur(myimage, 1)
 
    # We bin the pixels. Result will be a value 1..5
    # bins=np.array([0,51,102,153,204,255])
    # myimage[:,:,:] = np.digitize(myimage[:,:,:],bins,right=True)*51
 
    # Create single channel greyscale for thresholding
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)
 
    # Perform Otsu thresholding and extract the background.
    # We use Binary Threshold as we want to create an all white background
    background = cv2.threshold(myimage_grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
 
    # Convert black and white back into 3 channel greyscale
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
 
    # Perform Otsu thresholding and extract the foreground.
    # We use TOZERO_INV as we want to keep some details of the foregorund
    foreground = cv2.threshold(myimage_grey,0,255,cv2.THRESH_TOZERO_INV+cv2.THRESH_OTSU)[1]  #Currently foreground is only a mask
    foreground = cv2.bitwise_and(myimage,myimage, mask=foreground)  # Update foreground with bitwise_and to extract real foreground
 
    # Combine the background and foreground to obtain our final image
    finalimage = background+foreground
 
    return finalimage

def rotate(image: cv2.Mat, angle: float, background: tuple):
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

def removeLine(image: cv2.Mat):
    img2 = image.copy()
    height_ori, width_ori = img2.shape[:2]

    width_line = 1150
    height_line = int((height_ori/width_ori) * width_line)
    image2 = cv2.resize(img2, (width_line, height_line), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (1,1), 0)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (44,1))
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image2, [c], -1, (255,255,255), 3)

    # Remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,44))
    remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image2, [c], -1, (255,255,255), 3)

    # Repair image
    # repair_kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1,4))
    # result1 = 255 - cv2.morphologyEx(255 - img2, cv2.MORPH_CLOSE, repair_kernel1, iterations=1)

    # Combine masks and remove lines
    # table_mask = cv2.bitwise_or(remove_horizontal, remove_vertical)
    # img2[np.where(table_mask==255)] = [255,255,255]

    # size original
    res = cv2.resize(image2, (width_ori, height_ori),interpolation=cv2.INTER_CUBIC)

    return res

def increase_resolution(image: cv2.Mat, path_model: str):
    height, width = image.shape[:2]
    # print(height, width)
    if 2*width <= 4500:
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        # path = "LapSRN_x2.pb"
        sr.readModel(path_model)
        sr.setModel("lapsrn",2)
        result = sr.upsample(image)
        return result
    return image

def display_image(image: cv2.Mat):
    plt.figure(figsize = (12,9))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

def Noisy(noise_typ: str, image: cv2.Mat):
    if noise_typ == "gauss":
        row,col,ch= image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = image + gauss
        return noisy.astype(np.dtype('uint8'))
    elif noise_typ == "s&p":
        row,col,ch = image.shape
        s_vs_p = 0.2
        amount = 0.00004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in image.shape]
        out[coords] = 0
        return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy.astype(np.dtype('uint8'))
    elif noise_typ == "speckle":
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
        return noisy.astype(np.dtype('uint8'))

def BlurImg(blur_typ: str, img: cv2.Mat):
    if blur_typ == 'Averaging':
        return cv2.blur(img,(1,1))
    elif blur_typ == 'GaussianBlurring':
        return cv2.GaussianBlur(img,(5,5),0)
    elif blur_typ == 'MedianBlurring':
        return cv2.medianBlur(img,1)
    elif blur_typ == 'BilateralFiltering':
        return cv2.bilateralFilter(img,9,75,75)

def AddNoiseAndBlur(image: cv2.Mat, noise_typ: str, blur_typ: str):
    noise_img = Noisy(noise_typ,image)
    blur_img = BlurImg(blur_typ,noise_img)
    return blur_img

def adjust_gamma(image: cv2.Mat, gamma: str = 1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)