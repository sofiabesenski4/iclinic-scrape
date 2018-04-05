
import argparse
from pathlib import Path
import os
import pyautogui as auto
import PIL
import time
import datetime
import cv2
import numpy
img = numpy.array(auto.screenshot())

os.chdir("Screens")
os.mkdir("testing")
#[element.save(fp = os.path.join(p,index), format = "png") for index, element in enumerate(image_list)]
os.chdir("testing")
print(os.getcwd())
cv2.imwrite("testimage.png",img)	
