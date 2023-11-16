#!/usr/bin/env python

import winsound
import pyautogui
import time
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

#
# https://github.com/UB-Mannheim/tesseract/wiki
# Path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


###############################
# CONST
###############################
DEFAULT_SCREEN = (3840, 2160)


COMBAT_OFFSET = lambda vp: (int(vp[0]/2) - 420, int(vp[1] * 0.85), 820, 60)
END_OFFSET = lambda vp: (int(vp[0]/2) - 220, int(vp[1] * 0.85), 460, 60)


GRACE_PERIOD = 5
SOUND_HZ = 440
SOUND_MS = 3000

DEBUG = False

###############################
# CUSTOMIZABLE CONST
###############################

# sleep in between wave before looking for G button.
# this is to ensure that the image processing is done
# only when needed. 
WAVE_RUNTIME = 60




def validate_g_button(offset, error = 5):

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

        if len(text) >= error:
            return True

    return False


def wait_and_combat(vp):
    for _ in range(30):    
        found = validate_g_button(COMBAT_OFFSET(vp))

        if found:
            print("Pressing G")
            pyautogui.press("g")
            return

        print(f"Waiting for G button...")
        time.sleep(5)


def end_wave(vp):
    for _ in range(20):
        found = validate_g_button(END_OFFSET(vp))

        if found:
            print("Pressing G for ending wave")
            pyautogui.press("g")
            time.sleep(1)
            winsound.Beep(SOUND_HZ, SOUND_MS)            
            return

        print(f"Waiting for G button to end round...")
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
            if i % 5 == 0:
                print(f"Waiting {i} of {WAVE_RUNTIME} seconds")
            time.sleep(1)

        # wait for wave end animation   
        time.sleep(GRACE_PERIOD)

    end_wave(vp)
    waves = input("Restart Script? Re-enter number of waves: ")
    if len(waves) > 0:
        main_combat(vp, int(waves))
    else:
        print("Bye...")
        exit(0)


if __name__ == "__main__":
    viewport = pyautogui.size()
    print("Screen ", viewport)
    waves = input("Enter number of waves: ")
    main_combat(viewport, int(waves))
