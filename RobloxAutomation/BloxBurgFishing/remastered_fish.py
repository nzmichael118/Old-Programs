import pyautogui
import time
# Prevents pyauto gui from turning off
pyautogui.FAILSAFE = False

"""This script is designed to automattically fish in the BLOXBURG
   Fishing Minigame in order to gain money throughout a long period
   of time without requiring manual input from the player
   Working as of -- 19/06/2020 --  """


def Main():
    """ This function is designed to call other functions"""
    fishing_area = Get_Area() # Fishing area is a 4 int tuple
    time.sleep(1)
    Click() # This click is designed to get Roblox focused
    time.sleep(2)
    while True: # The main loop of the script in which the player farms on
        pixel_location = (0, 0)
        while pixel_location == (0, 0): # Gets white pixel to watch
            time.sleep(2)
            capture = Take_Screenshot(fishing_area)
            pixel_location = Find_Pixel(capture, fishing_area[2], fishing_area [3])
            if pixel_location == (0, 0):
                print("Something went wrong, Fixing now...")
                Click() # Fixes if a popup appears and breaks the script
        white_location = (fishing_area[0] + pixel_location[0],\
        fishing_area[1] + pixel_location[1])
        Watch_Pixel(white_location)
        time.sleep(2)
        Click()





def Click():
    """Clicks without needing to type out the entire command"""
    pyautogui.click()

def Get_Area():
    """ This function is made to get the dimentions of the fishing area"""
    wait_delay = 2
    # Gets top left location
    print("Please put your cursor in the top left of the fishing area...")
    time.sleep(wait_delay)
    start_location = pyautogui.position()
    print("Start coordinates are at {}".format(start_location))
    # Gets bottom right location
    print("Please put your cursor in the bottom right of the fishing area...")
    time.sleep(wait_delay)
    end_location = pyautogui.position()
    print("End coordinates are at {}".format(end_location))
    
    # Convert the end location to the width and height
    width = end_location[0] - start_location[0]
    height = end_location[1] - start_location[1]

    return((start_location[0], start_location[1], width, height)) # Returns as a tuple

def Take_Screenshot(screenshot_location):
    capture = pyautogui.screenshot(region=(screenshot_location))
    return(capture)

def Find_Pixel(capture, width, height):
    concecutives = 0 # Used to find how many whites in a row
    max_concecutive = 5 # Threshold
    min_brightness = 60
    watch_location = (0, 0)

    # Scroll through all pixels and find 5 pixels in a row where RGB are the same
    for y in range (height):
        if watch_location == (0, 0):
            concecutives = 0
            for x in range(width):
                color_value = capture.getpixel((x,y))
                # Returns a tuple with RGB valuese
                if color_value[0] == color_value[1] == color_value[2] and color_value[0] >= min_brightness:
                    concecutives += 1
                    if concecutives >= max_concecutive:
                        watch_location = (x, y)
                        print("Found Pixel with RGB value {} at {}".format(color_value, watch_location))
                        break
                else:
                    concecutives = 0
        else:
            break   
    # For loop finishes here
    return(watch_location)
    
def Watch_Pixel(location):
    
    moved = False
    while moved == False:
        capture = pyautogui.screenshot(region=(location[0], location[1], 1, 1))
        values = capture.getpixel((0,0))
        if values[0] != values[1] != values[2]:
            print("Moved RGB value changed to {}".format(values))
            Click()
            moved = True

# Calls the main function which calls other functions
Main()