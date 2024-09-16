"""This is a reformed version of some education perfect cheats.
        - Programmed during: 20/02/2021
 """
import time
import pyautogui
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = \
    'C:/Program Files/Tesseract-OCR/tesseract.exe'

translations_dictionary = {}

def main():
    # Get the dimensions of the main screenspace and the answer screenspace 
    main_screenspace = define_area()

    # Brings up the unknown tab
    print("Typing")
    type_output("?")
    time.sleep(1)
    print("Answer screenshot")
    answer_screenspace = define_area()
    type_output(screenshot_to_text(answer_screenspace))

    while True:
        pyautogui.press('backspace', presses=50)
        time.sleep(2)
        question = screenshot_to_text(main_screenspace)
        if question in translations_dictionary:
            print(f"'{question}' : '{translations_dictionary[question]}''")
            type_output(translations_dictionary[question])
        else:
            type_output("?")
            time.sleep(0.5)
            translations_dictionary[question] = \
                screenshot_to_text(answer_screenspace)
            print(f"'{question}'' : '{translations_dictionary[question]}''")
            type_output(translations_dictionary[question])
            time.sleep(1)


def type_output(output):
    """Simulates keyboard input using pyautogui module
    and will press "enter" after  """
    try:
        pyautogui.write(output, interval=0.005)
        pyautogui.press("enter")
    except Exception:
        print(f"Error: Cannot type {output}")


def take_screenshot(screenspace):
    """Takes a screenshot of given screenspace and return it"""
    return(pyautogui.screenshot(region = (screenspace)))


def read_image(capture):
    """Uses tesseract to read the screenshot and will 
    return to a string if a read fails will return "?" """
    try:
        output_string = pytesseract.image_to_string(capture, timeout=3)
        # It may seem counter intuitive to convert to a string but this
        # is for error capturing with timeouts
        output_string = str(output_string)
        if len(output_string) > 0:

            # Sanitizing input
            output_string = output_string.replace("|", "I")
            output_string = output_string.replace("\n", " ")
            output_string = output_string.replace("Copy the answer above", "")
            output_string = output_string.replace("Kopy the answer above", "")
            output_string = output_string.replace("opy the answer above", "")
            output_string = output_string.replace("Translate from English to Spanish", "")
            output_string = output_string.replace("Translate from Spanish to English", "")

            output_string = output_string.split(",")
            return(output_string[0])

        else:
            print(f"Error in reading screenshot...")
            return("?")
    except Exception:
        print("!BAD READ!")
        return("?")


def screenshot_to_text(screenspace):
    """Combines the functions take_screenshot() and read_image() 
    and returns the output of read_image() saving lines in the main
    function"""
    return(read_image(take_screenshot(screenspace)))


def define_area():
    """Uses a previously used method of using cursor position in order
    to define a screen area in which the script needs to reference,
    will return a tuple containing four pieces of information"""
    sleep_delay = 3

    # Gets mouse positions
    print("Please place your cursor at the top left of the text")
    time.sleep(sleep_delay)
    start_coords = pyautogui.position()
    print("Please place your cursor at the bottom right of the text")
    time.sleep(sleep_delay)
    end_coords = pyautogui.position()

    # Math to generate Width and Height
    width = end_coords[0] - start_coords[0]
    height = end_coords[1] - start_coords[1]

    # Returns Tuple used to take screenshots of selected area
    return((start_coords[0], start_coords[1], width, height))


if __name__ == "__main__":
    main()