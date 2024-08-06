import time
import pyautogui
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
pytesseract.tessedit_char_whitelist ='0123456789+-*'
def main():
    q_sc, q_w, q_h = Find_Area() # question start coords, width then height
    a1_sc, a1_w, a1_h = Find_Area()
    a2_sc, a2_w, a2_h = Find_Area()
    a3_sc, a3_w, a3_h = Find_Area()
    a4_sc, a4_w, a4_h = Find_Area()

    while True:
        question_cap = Take_screenshot(q_sc, q_w, q_h)
        q_string = Read_img(question_cap)
        q_ans = (calc_math(q_string))

        try:
            if q_ans == int(Read_img(Take_screenshot(a1_sc, a1_w, a1_h))):
                print("moving to a1")
                click_on(a1_sc)
        except Exception:
            print("Read Error")
        try:
            if q_ans == int(Read_img(Take_screenshot(a2_sc, a2_w, a2_h))):
                print("moving to a2")
                click_on(a2_sc)
        except Exception:
            print("Read Error")

        try:
            if q_ans == int(Read_img(Take_screenshot(a3_sc, a3_w, a3_h))):
                print("moving to a3")
                click_on(a3_sc)
        except Exception:
            print("Read Error")
        try:
            if q_ans == int(Read_img(Take_screenshot(a4_sc, a4_w, a4_h))):
                print("moving to a4")
                click_on(a4_sc)
        except Exception:
            print("Read Error")

        
        print("Answer was {}".format(q_ans))



        time.sleep(1)


def click_on(location):
    pyautogui.moveTo(location)
    time.sleep(0.5)
    pyautogui.click(location)
    pyautogui.click(location)
    pyautogui.hotkey('alt', 'tab')




def calc_math(raw):
    calc = 0
    try:
        raw = raw.replace(" ", "")
        if "-" in raw:
            # minus function
            raw = raw.split("-")
            calc = int(raw[0]) - int(raw[1])

        elif "+" in raw:
            # addition function
            raw = raw.split("+")
            calc = int(raw[0]) + int(raw[1])

        elif "*" in raw:
            # multiplication function
            raw = raw.split("*")
            calc = int(raw[0]) * int(raw[1])
    except Exception:
        return(0)
    return(calc)


def Find_Area():
    """Used to find the start and end area to where one would take a screenshot"""
    sleep_delay = 1
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


def Read_img(capture):
    """Will read the image and return the raw text from image using PYTESSERACT """

    read_text = pytesseract.image_to_string(capture, timeout=3)

    return(read_text)



if __name__ == "__main__":
    main()