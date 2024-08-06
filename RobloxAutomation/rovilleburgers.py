"""RoVille burgatory minigame autofarmer"""
try:
    import pyautogui
    from PIL import Image
    import pytesseract
    import time
    import ctypes

except ImportError:
    print("Import Error: Please make sure you have installed" \
    " all the required packages")
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
pyautogui.FAILSAFE = False

def get_coords():
    # Monitor
    time_delay = 2

    print("Place your cursor on the top left of the monitor")
    time.sleep(time_delay)
    coords_1 = pyautogui.position()


    print("Place your cursor on the bottom right of the monitor")
    time.sleep(time_delay)
    coords_2 = pyautogui.position()

    # Turn X point 2 into a coord
    width = coords_2[0] - coords_1[0]
    height = coords_2[1] - coords_1[1]

    # Buttons
    print("Place Cursor over burger")
    time.sleep(time_delay)
    burger = pyautogui.position()
    print("Place Cursor over Cola")
    time.sleep(time_delay)
    cola = pyautogui.position()
    print("Place Cursor over fries")
    time.sleep(time_delay)
    fries = pyautogui.position()
    return(coords_1, width, height, burger, cola, fries)

def take_screenshot(coord_1, width, height):
    capture = pyautogui.screenshot( \
    region = (coord_1[0] , coord_1[1], width, height))
    read_text = pytesseract.image_to_string(capture, timeout=2)
    print(read_text)
    return(read_text)

def place_order(burger, cola, fries, order):
    click_delay = 0.1
    if "bu" in order.lower():
        #pyautogui.moveTo(burger, duration=0.01)
        ctypes.windll.user32.SetCursorPos(burger[0], burger[1])
        print("Moving to Burger")
        time.sleep(click_delay)
        pyautogui.click()
        pyautogui.click()
        time.sleep(click_delay)
        pyautogui.hotkey('alt', 'tab')


    elif "co" in order.lower():
        #pyautogui.moveTo(cola, duration=0.01)
        ctypes.windll.user32.SetCursorPos(cola[0], cola[1])
        print("Moving to cola")
        time.sleep(click_delay)
        pyautogui.click()
        pyautogui.click()
        time.sleep(click_delay)
        pyautogui.hotkey('alt', 'tab')


    elif "fr" in order.lower():
        #pyautogui.moveTo(fries, duration=0.01)
        ctypes.windll.user32.SetCursorPos(fries[0], fries[1])
        print("Moving to fries")
        time.sleep(click_delay)
        pyautogui.click()
        pyautogui.click()
        time.sleep(click_delay)
        pyautogui.hotkey('alt', 'tab')


    elif "a" in order.lower():
        #pyautogui.moveTo(fries, duration=0.01)
        ctypes.windll.user32.SetCursorPos(fries[0], fries[1])
        print("Moving to fries")
        time.sleep(click_delay)
        pyautogui.click()
        pyautogui.click()
        time.sleep(click_delay)
        pyautogui.hotkey('alt', 'tab')

            

point_1, width, height, burger, cola, fries = get_coords()
while True:

    order = take_screenshot(point_1, width, height)
    place_order(burger, cola, fries, order)
    time.sleep(1)