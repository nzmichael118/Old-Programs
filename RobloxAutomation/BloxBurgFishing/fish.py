#try:
import pyautogui
import time
from PIL import Image
import sys
import numpy as np
pyautogui.FAILSAFE = False
#except ImportError:
#    print("Import Error")
min_red = 55
max_bg = 13

def Find_Area():
    sleep_delay = 1
    print("Please put your cursor in the top left of your fishing area")
    time.sleep(sleep_delay)
    start_coords = pyautogui.position()
    print("Please put your cursor in the bottom right of your fishing area")
    time.sleep(sleep_delay)
    end_coords = pyautogui.position()
    width = end_coords[0] - start_coords[0]
    height = end_coords[1] - start_coords[1]
    print(start_coords, width, height)
    return(start_coords, width, height)

def Take_screenshot(start_tuple, width, height):
    capture = pyautogui.screenshot(\
    region = (start_coords[0], start_coords[1], width, height)) 

    return(capture)


def Find_Red_Pixel(capture, width, height):
    max_red = 0
    watch_location = (0, 0)
    for x in range(width):
        if watch_location [0] == 0 :
            for y in range(height):
                color = capture.getpixel((x,y))
                if color [0] > max_red:
                    max_red = color[0]
                if color[0] > min_red and color[1] < max_bg and color [2] < max_bg:
                    print("red")
                    print(color)
                    watch_location = (x, y)
                    print(watch_location)
                    break
        else:
            break
    print(max_red)
    return(watch_location)

def Watch_pixel(pixel_location, corner_coords):    
    moved = False
    location_x = corner_coords[0] + pixel_location[0]
    location_y = corner_coords[1] + pixel_location[1]
    while moved == False:
        photo = pyautogui.screenshot(region=(location_x, location_y, 1, 1))
        values = photo.getpixel((0,0))
        if values[2] > max_bg or values[0] < min_red:
            time.sleep(0.5)
            print("Moved")
            moved = True
            click()

def click():
    pyautogui.click()           
# Calling functions bellow

def Do_stuff():
    capture = Take_screenshot(start_coords, width, height)
    time.sleep(0.1)
    pixel = Find_Red_Pixel(capture, width, height)
    return pixel

start_coords, width, height = Find_Area()
time.sleep(1)
click()
click()
time.sleep(2)
while True:

    pixel = Do_stuff()
    Watch_pixel(pixel, start_coords)
    time.sleep(2)
    click()
    time.sleep(2)

