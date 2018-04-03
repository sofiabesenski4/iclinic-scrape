#iclinic_scraping.py
import pyautogui as auto
import PIL
import time
#zoom in to the desired view for good OCR
"""
auto.keyDown('ctrl')
auto.scroll(6)
auto.keyUp('ctrl')
"""
SEARCHBAR_LOCATION =(1281,125)

SCROLLDOWN_BUTTON_LOCATION = (1917,737)
PATIENTLIST_RESULT_AREA = (1118,200,713,546)


#automating a single query and series of clicks
auto.moveTo(SEARCHBAR_LOCATION)
auto.click()
auto.click()
auto.press('backspace')
auto.press('backspace')
auto.press('backspace')
auto.press('backspace')
auto.press('backspace')
auto.press('backspace')
auto.press('backspace')
auto.press('backspace')
auto.press('backspace')
auto.press('backspace')
auto.typewrite('01/01/1953')
auto.press('enter')
time.sleep(2)
im1 = auto.screenshot(region = PATIENTLIST_RESULT_AREA)
auto.moveTo(SCROLLDOWN_BUTTON_LOCATION)
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
auto.click()
time.sleep(1)
im2 = auto.screenshot(region = PATIENTLIST_RESULT_AREA)
im1.show()
im2.show()
