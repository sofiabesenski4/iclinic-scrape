#iclinic_scraping.py

"""
This should save every feasable DOB's patient list into folders which
will take up <50GB.

Before running script, open google chrome and sign into the iclinic
emr portal and zoom in to 150%
Pseudocode:

open a connection to the DB
for enumerate(every date from 01-01-1900 to present):
	clear searchbox
	enter the date
	allow 1 sec to load
	screen cap the table
	scroll down the menu
	screen cap the table
	scroll down the menu
	screen cap the table
	save all screen caps in a folder labelled by the "<year>-<month>"
	
	
"""

#import all the modules
import numpy
import cv2
import argparse
from pathlib import Path
import os
import pyautogui as auto
import PIL
import time
import datetime


#These are all constants which are specific to the computer monitor in the office
SEARCHBAR_LOCATION =(1281,125)
SCROLLDOWN_BUTTON_LOCATION = (1917,737)
PATIENTLIST_RESULT_AREA = (1118,200,713,546)
FIRST_PATIENT_LOCATION =(1432,214)
MIN_DATE_ORDINAL = 693596
#MIN_DATE_ORDINAL = 714446
#this date corresponds to jan 1, 1910
MAX_DATE_ORDINAL = 697248



def clear_search_box():
	auto.moveTo(SEARCHBAR_LOCATION)
	auto.click()
	auto.click(clicks=2)
	for i in range(0,10):
		auto.press('backspace')

def scroll_to_next_page():
	for i in range(0,16):
		auto.press('down')

def search_DOB(current_ordinal_date):
	clear_search_box()
	current_date = datetime.date.fromordinal(current_ordinal_date)
	auto.typewrite(str(current_date.month).zfill(2) + "/" + str(current_date.day).zfill(2)+ "/"+ str(current_date.year))
	auto.press('enter')
	
#Function to be called when the date has been searched and we want to capture 3 full page screenshots
def cap_tables():
	img1 = auto.screenshot(region = PATIENTLIST_RESULT_AREA)
	auto.moveTo(FIRST_PATIENT_LOCATION)
	auto.click()
	scroll_to_next_page()
	img2 = auto.screenshot(region = PATIENTLIST_RESULT_AREA)
	scroll_to_next_page()
	img3 = auto.screenshot(region = PATIENTLIST_RESULT_AREA)
	return (img1,img2,img3)

 
"""
open a connection to the DB
for enumerate(every date from 01-01-1900 to present):
	clear searchbox
	enter the date
	allow 1 sec to load
	screencapture the tables
	save all screen caps in a folder labelled by the "<year>-<month>"

"""	
	
def main():	
	ap = argparse.ArgumentParser()
	ap.add_argument("--db","--database",required =False)
	args = ap.parse_args()
	
	
	current_month = 1
	date_index = MIN_DATE_ORDINAL
	#while there are still dates
	os.chdir("Screens")
		
	while date_index < MAX_DATE_ORDINAL:	
		#while we are in one month
		image_list = []
		while datetime.date.fromordinal(date_index).month == current_month: 
			clear_search_box()
			search_DOB(date_index)
			time.sleep(1)
			screen_caps = cap_tables()
			
			[image_list.append(element) for element in screen_caps]
			
			date_index+=1
		
		#list comprehension to write each of those PIL images to a folder in the directory "Screens"
		os.mkdir("{}-{}".format(datetime.date.fromordinal(date_index).year, current_month))
		os.chdir("{}-{}".format(datetime.date.fromordinal(date_index).year, current_month))
		[cv2.imwrite("{}.png".format(str(index)),numpy.array(element)) for index, element in enumerate(image_list)]
		
		os.chdir("..")
		current_month = datetime.date.fromordinal(date_index).month
		

if __name__ == "__main__":
	main()
	
