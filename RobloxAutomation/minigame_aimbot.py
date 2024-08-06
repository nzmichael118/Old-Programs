import time
import pyautogui
from PIL import Image
from pynput.keyboard import Key, Controller
#(36, 37, 39)

pyautogui.FAILSAFE = False
keyboard = Controller()


def main():
    start, width, height = Find_Area()
    while not keyboard.press("a"):
        capture = Take_screenshot(start, width, height)
        location = Find_pixel(capture, width, height, start)
        if location != None:
            pyautogui.click(location)
            pyautogui.click()  
            pyautogui.hotkey('alt', 'tab')
        else:
            print("Cannot Find")
        location = None


def Find_Area():
    """Used to find the start and end area to where one would take a screenshot"""
    sleep_delay = 2
    print("Please put your cursor in the top left of text")
    time.sleep(sleep_delay)
    start_coords = pyautogui.position()
    print("Please put your cursor in the bottom right of your text")
    time.sleep(sleep_delay)
    end_coords = pyautogui.position()
    width = end_coords[0] - start_coords[0]
    height = end_coords[1] - start_coords[1]
    print(start_coords, width, height)
    return(start_coords, width, height)

    
def Take_screenshot(start_coords, width, height):
    """Takes screenshot of given area """
    capture = pyautogui.screenshot(\
    region = (start_coords[0], start_coords[1], width, height)) 
    return(capture)

def Find_pixel(capture, width, height, sc):
    # (36, 37, 39)
    pixel_val = (111, 121, 144)
    for y in range(height):
        for x in range(width):
            color_val = capture.getpixel((x,y))
            if color_val == pixel_val:
                return(((sc[0] + x), (sc[1] + y)))




if __name__ == "__main__":
    main()