#!/usr/bin/env python

import winsound
import pyautogui
import time
import pytesseract
from enum import Enum
from PIL import Image, ImageEnhance, ImageFilter
from config import tesseract_path, sound_in_milliseconds, wave_run_time

#
# https://github.com/UB-Mannheim/tesseract/wiki
# Path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = tesseract_path



###############################
# CONST
###############################
UHD_SCREEN = (3840, 2160, 0.85, 0.75)
FHD_SCREEN = (1920, 1080, 0.77, 0.70)
OTHER_SCREEN = (0, 0, 0.80, 0.75)


COMBAT_OFFSET = lambda vp: (int(vp[0]/2) - 420, int(vp[1] * vp[2]), 820, 60)
END_OFFSET = lambda vp: (int(vp[0]/2) - 220, int(vp[1] * vp[2]), 460, 60)
RETRY_OFFSET = lambda vp: (int(vp[0]/2) - 420, int(vp[1] * vp[3]), 820, 60)

class Button(Enum):
    NONE = 0
    CONTINUE = 1
    RETRY = 2

###############################
# CUSTOMIZABLE CONST
###############################

# Sleep in between wave before looking for G button.
# this is to ensure that the image processing is done
# only when needed. 
WAVE_RUNTIME = wave_run_time

# Additional wait time at the end of each round for the green gem animation
GRACE_PERIOD = 5

# Custom beep sound to alert user that the run is done
SOUND_MS = sound_in_milliseconds
SOUND_HZ = 440

# Set to True to see more logging and processed images
DEBUG = False



def validate_button(offset, error = 5):

    for i in range(5):

        time.sleep(0.2)
        im = pyautogui.screenshot(region=offset)

        # erosion -> dilation
        im = im.filter(ImageFilter.MinFilter(3))
        im = im.filter(ImageFilter.MaxFilter(3))
        
        # enhance different between text and background
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(2)

        # enhance text's edges
        sharper = ImageEnhance.Sharpness(im)
        im = sharper.enhance(1)
        
        # enhance text color quality
        colorer = ImageEnhance.Color(im)
        im = colorer.enhance(2)

        # to gray scale
        im = im.convert("1")
        text = ""
        if DEBUG:
            im.save(f"temp{i}.jpg")
            text = pytesseract.image_to_string(Image.open(f"temp{i}.jpg"))
        else:
            text = pytesseract.image_to_string(im)

        text = text.strip()
        if DEBUG:
            print(f"Detected: {text}")

        if ("YES" in text) or ("NO" in text):
            return Button.RETRY 

        if len(text) >= error:
            return Button.CONTINUE

    return Button.NONE


def wait_and_combat(vp):
    for _ in range(30):    
        foundBtn = validate_button(COMBAT_OFFSET(vp))

        if foundBtn == Button.CONTINUE:
            print("Pressing G")
            pyautogui.press("g")
            return

        foundBtn = validate_button(RETRY_OFFSET(vp))
        if foundBtn == Button.RETRY:
            print("Pressing Y")
            pyautogui.press("y")
            winsound.Beep(SOUND_HZ, SOUND_MS)
            raise ValueError("RETRY")

        print(f"Waiting for the G button...")
        time.sleep(5)


def end_wave(vp):
    for _ in range(30):
        foundBtn = validate_button(END_OFFSET(vp))

        if foundBtn == Button.CONTINUE:
            print("Pressing G for ending wave")
            pyautogui.press("g")
            winsound.Beep(SOUND_HZ, SOUND_MS)
            return

        foundBtn = validate_button(RETRY_OFFSET(vp))
        if foundBtn == Button.RETRY:
            print("Pressing Y")
            pyautogui.press("y")
            winsound.Beep(SOUND_HZ, SOUND_MS)
            raise ValueError("RETRY")

        print(f"Waiting for the G button to end round...")
        time.sleep(5)


def main_combat(vp, waves):
    print(f"Starting in...")
    for i in range(5, -1, -1):
        print(i)
        time.sleep(1)

    for w in range(waves):
        wait_and_combat(vp)

        print(f"Running Wave: {w+1} of {waves}")

        # wait for the wave to end
        for i in range(WAVE_RUNTIME):
            if i % 10 == 0:
                print(f"Waiting {i} of {WAVE_RUNTIME} seconds")
            time.sleep(1)

        # wait for wave end animation   
        time.sleep(GRACE_PERIOD)

    end_wave(vp)
    waves = input("Re-enter number of waves (empty to exit): ")
    if len(waves) > 0:
        main_combat(vp, int(waves))
    else:
        print("Bye...")
        exit(0)


def get_screen_ratio(vp):
    w, h = vp

    if h == UHD_SCREEN[1]:
        return UHD_SCREEN
    elif h == FHD_SCREEN[1]:
        return FHD_SCREEN
    else:
        return (w, h, OTHER_SCREEN[2], OTHER_SCREEN[3])

if __name__ == "__main__":
    viewport = pyautogui.size()
    print("Screen ", viewport)

    waves = input("Enter number of waves: ")
    try:
        main_combat(get_screen_ratio(viewport), int(waves))
    except ValueError as e:
        if str(e) != "RETRY":
            raise
        else:
            waves = input("Re-enter number of remaining waves (empty to exit): ")
            if len(waves) > 0:
                main_combat(get_screen_ratio(viewport), int(waves))
            else:
                print("Bye...")
                exit(0)
