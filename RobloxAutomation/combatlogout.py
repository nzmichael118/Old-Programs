import pyautogui

#                    *deadname*:0    Michael:1   Jerry:2
resolution_profiles = [(1783,20), (2423, 20), (1783, 48)]
profile = 1
def main():
    pos = setup_viewfinder()

    healthy = True
    print("it is working...")
    while(healthy):
        # get rgb
        capture = pyautogui.screenshot(region = (pos[0], pos[1], 1, 1))
        rgb = capture.getpixel((0,0))

        # Test pixel
        if rgb[0] > 240:
            if rgb[1] < 60 and rgb[2] < 40:
                quit_game(rgb)

def setup_viewfinder():
    return(resolution_profiles[profile])

def quit_game(rgb_value):
    print(rgb_value)
    pyautogui.hotkey('alt', 'f4')



if __name__ == "__main__":
    main()