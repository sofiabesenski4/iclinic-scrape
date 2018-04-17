
#using pytesseract as the ocr engine
import pytesseract
##using opencv to feed image input into tesseract
import cv2
import PIL
import os
#PIL is the python imaging library, used by opencv
from PIL import ImageFilter
#PIL uses numpy to represent images
import numpy as np
from PIL import Image


#https://stackoverflow.com/questions/42045362/change-contrast-of-image-in-pil
def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

os.chdir("Screens/1900-1")

image_list = ["0.png","74.png"]
for image_name in image_list:
	#print(image)
	temp = Image.open(image_name)
	#temp = temp.filter(PIL.ImageFilter.GaussianBlur(0.01))
	#col = change_contrast(Image.open(image_name), 30)
	#print(image.shape)
	
	#gray = col
	#gray = temp.convert('L')	
	bw = temp.point(lambda x: 0 if x<200 else 255)
	#gray = gray.filter(ImageFilter.FIND_EDGES)
	#cleaned_image_name = str(os.getpid()) + '_cleaned.jpg'
	#bw.save(cleaned_image_name)
	#gray = cv2.imread(image_name)
	#gray  = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
	#gray = image
	"""HERE IS WHERE WE CAN ADD IN OUR OWN FILTERS/PREPROCESSING EFFECTS TO INCREASE OCR ACCURACY DEPENDING ON DATA
	"""
	#check to see if we are applying a thresholding to preprocess the image
	
	#gray = cv2.threshold(gray, 200,255,cv2.THRESH_OTSU)[1]
	#gray = cv2.threshold(gray, 200, 255, cv2.THRESH_TOZERO)[1]
	#gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)[1]
	#bw = cv2.medianBlur(bw,3)
	#write the image file temporarily to disk so we can OCR it with the pytesseract interface, accessing
	# the (natively Java) tesseract application 
	#cv2.imshow("img,",image)
	
	
	
	filename = "{}.png".format(os.getpid())
	bw.save(filename)


	#we can finally apply tesseract to the saved image using python bindings, while removing the temp image from disk
	text = pytesseract.image_to_string(Image.open(filename), lang = "eng", boxes = False, config = "")
	print(text)
	#cv2.imshow("Image",image)
	#cv2.imshow("Output", gray)
	
	#os.remove(filename)
