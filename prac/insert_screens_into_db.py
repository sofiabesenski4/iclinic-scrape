#insert_screens_into_db.py
from pg import DB
#using pytesseract as the ocr engine
import pytesseract
import argparse
##using opencv to feed image input into tesseract
import cv2
import PIL
import os
#PIL is the python imaging library, used by opencv
from PIL import *
#PIL uses numpy to represent images
import numpy as np
import re
import datetime
from PIL import Image
from PIL import ImageFilter
"""
pseudocode:

Enter the Screens directory:
	for each folder in this directory (os.dirlist):
		enter folder 
		for every image:
			OCR it
			extract each first name, last name, PHN, DOB and store each as a tuple
			add each tuple to a set
		convert set of tuples to a list and inserttable into the db

"""
def main():
	#enter screens
	os.chdir("Screens")
	
	extracted_patient_tuples = []
	extracted_patient_nonmatches = []
	print(os.getcwd())
	for folder in os.listdir(os.getcwd()):
	#	print("here")
		folder_path = os.path.join(os.getcwd(),folder)
		print(folder_path)
		
		for image in os.listdir(folder_path):
			#call to ocr
			#print(image)
			#print(cv2.imread(os.path.join(folder_path, image)).shape)
			text = OCR_img(Image.open(os.path.join(folder_path, image)))
			
			#append to the list of found patients in this folder
			[extracted_patient_tuples.append(element) for element in extract_patient_info(text)[0]]
			[extracted_patient_nonmatches.append(element) for element in extract_patient_info(text)[1]]
		extracted_patient_tuples = list(set(extracted_patient_tuples))
	os.chdir("..")
	fp = open("mismatches.txt","a")
	[fp.write(element + "\n") for element in extracted_patient_nonmatches]
	print(extracted_patient_tuples)
	insert_patient_set_into_db(DB("test_patients"), extracted_patient_tuples)
	
	return

def OCR_img(image_file):
	
	#cv2.imshow("img",image_file)
	#gray = cv2.medianBlur(image_file,3)
	#gray  = cv2.cvtColor(image_file,cv2.COLOR_BGR2GRAY)
	#gray = image_file.filter(PIL.ImageFilter.GaussianBlur(0.01))
	
	gray = image_file.point(lambda x: 0 if x<200 else 255)
	#gray = image_file
	"""HERE IS WHERE WE CAN ADD IN OUR OWN FILTERS/PREPROCESSING EFFECTS TO INCREASE OCR ACCURACY DEPENDING ON DATA
	"""
	#check to see if we are applying a thresholding to preprocess the image
	"""if args.preprocess == "thresh" :
	"""
	#gray = cv2.threshold(gray, 150, 256, cv2.THRESH_OTSU)[1]
	"""
	#make a check to see if median blurring should be done to remove noise
	elif args.preprocess=="blur":
	gray = cv2.medianBlur(gray,3)
	"""	
	#write the image file temporarily to disk so we can OCR it with the pytesseract interface, accessing
	# the (natively Java) tesseract application 
	
	
	filename = "{}.png".format(os.getpid())
	gray.save(filename)
	

	#we can finally apply tesseract to the saved image using python bindings, while removing the temp image from disk
	text = pytesseract.image_to_string(Image.open(filename), lang = 'eng', config = '-psm 6')
	#print(text)
	os.remove(filename)	
	return text
#takes a block of text, each patient is separated by a newline character
"""Cramer, Riley XXX Test, Test Private 12/05/2000 17
HENDRIE, RYAN TE5T,0NLV 9048182075 08/15/1974 43
Mouse (WCA), Mickey X TEST Private 01/09/1924 94
TEST LABEL, Unknown TEST LABEL, private 01/01/2002 16
TEST, ONLV DAN-O private 01/01/1952 66
TEST, PATIENT 9059648172 02/01/1966 52
TEST, PATIENT (Sue) private

Test, Roxanne 8888888888 12/29/1977 40
test, support Private 08/01/2017 0
Test, Test Private 10/07/1997 20
Test, Test Private 07/01/2017 0
Test, Test Private 07/01/2017 0
Test, Test T Private 10/22/1957 60
Test, Tester 123456789
"""

def extract_patient_info(raw_text):
	patient_lines = raw_text.split('\n')
	#group 1 : last name, 2: first name, 3: PHN, 4: DOB
	patient_pattern = re.compile(r'(\w+?),? (\w+).* ((?:\d(?:\s?)){10}) (\d\d/\d\d/\d\d\d\d) \w*')
	#print(patient_lines)
	#tuples have the form (last_name,first_name,PHN,DOB)
	list_of_patient_tuples = []
	list_of_nonmatches = []
	for patient in patient_lines:
		if re.search(patient_pattern, patient) is not None:
			date_elements = re.search(patient_pattern, patient).group(4).split("/")
			datetime_object = datetime.date(month = int(date_elements[0]),year = int(date_elements[2]), day = int(date_elements[1])).isoformat()
			list_of_patient_tuples.append((re.sub(" ", "", re.search(patient_pattern, patient).group(3)),re.search(patient_pattern, patient).group(2),re.search(patient_pattern, patient).group(1),datetime_object))
		else:
			if re.search(r'create new patient|‘ l—I|‘ l—',patient):
				continue
			list_of_nonmatches.append(patient)
	#return format will be a tuple of lists of tuples, first list represents patient lines which were correctly identified,
	# second list represents patient lines which were not correctly interpretted
	#print(list_of_patient_tuples)
	#print(list_of_nonmatches)
	return (list_of_patient_tuples,list_of_nonmatches)	
"""
def insert_patient_tuples_into_db(db_ptr, patient_tuples):
	#tuples are of the form: (new_patient_phn,new_patient_first_name,new_patient_last_name,new_patient_dob_datetime_obj)
	try:
		assert "public.patients" in db_ptr.get_tables()
	except AssertionError:
		print("could not find public.patients db in patients_db_test on system")
		return
	try:
		assert  "phn" and "first_name" and "last_name" and "dob" in db_ptr.get_attnames("public.patients")
	except AssertionError:
		print("could not find required column names: dob, phn, first_name, or last_name")
		return
	db_ptr.inserttable("public.patients",patient_tuples)
	return
"""
def insert_patient_set_into_db(db_ptr, patient_set):
	#tuples are of the form: (new_patient_phn,new_patient_first_name,new_patient_last_name,new_patient_dob_datetime_obj)
	try:
		assert "public.patients" in db_ptr.get_tables()
	except AssertionError:
		print("could not find public.patients db in patients_db_test on system")
		return
	try:
		assert  "phn" and "first_name" and "last_name" and "dob" in db_ptr.get_attnames("public.patients")
	except AssertionError:
		print("could not find required column names: dob, phn, first_name, or last_name")
		return
	db_ptr.inserttable("public.patients",patient_set)
	return 

if __name__ == "__main__":
	main()
	
	
	
