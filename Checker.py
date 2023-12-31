
from Config import tesseract_path, debug
import time
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import pyautogui


###############################
# CONST
###############################
BUILD_OFFSET = (1700, 1836, 460, 60)
COMBAT_OFFSET = (1500, 1836, 820, 60)
END_OFFSET = (1700, 1836, 460, 60)
RETRY_OFFSET = (1500, 1620, 820, 60)
MENU_OFFSET = (2240, 1841, 460, 60)
WAVE_OFFSET = (3456, 50, 200, 100)

CURSOR_HEIGHT = 50

###############################
# CONST
###############################
# Only support 16:9 screen ratio
UHD_SCREEN = (3840, 2160, 1)
QHD_SCREEN = (2560, 1440, 2/3)
FHD_SCREEN = (1920, 1080, 1/2)

#
# https://github.com/UB-Mannheim/tesseract/wiki
# Path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = tesseract_path


class Checker():

    def __init__(self, name, offset, viewport, checkerFn):
        self.name = name
        self.checkerFn = checkerFn
        self.check_viewport(offset, viewport)

    def check_viewport(self, offset, viewport):
        w, h = viewport
        if h == UHD_SCREEN[1]:
            self.offset = tuple(int(d * UHD_SCREEN[2]) for d in offset)
            self.scale = UHD_SCREEN[2]
            return
        if h == QHD_SCREEN[1]:
            self.offset = tuple(int(d * QHD_SCREEN[2]) for d in offset)
            self.scale = QHD_SCREEN[2]
            return
        if h == FHD_SCREEN[1]:
            self.offset = tuple(int(d * FHD_SCREEN[2]) for d in offset)
            self.scale = FHD_SCREEN[2]
            return

        raise Exception(f"Unhandled Viewport {viewport}")

    def exec_debug(self):
        time.sleep(0.2)
        im = pyautogui.screenshot(region=self.offset)
        im.save(f"{self.name}_debug.jpg")
        print(f"Saved {self.name}_debug.jpg: ", self.offset)

    def exec(self):
        for i in range(5):

            time.sleep(0.2)
            im = pyautogui.screenshot(region=self.offset)

            # erosion -> dilation -> threshold
            im = im.filter(ImageFilter.MinFilter(3))
            im = im.filter(ImageFilter.MaxFilter(3))
            im = im.point(lambda p: 255 if p > 15 else 0)
            
            # enhance text's edges
            im = im.filter(ImageFilter.EDGE_ENHANCE)

            # enhance different between text and background
            enhancer = ImageEnhance.Contrast(im)
            im = enhancer.enhance(2)

            # to gray scale
            im = im.convert("1")
            text = ""
            if debug:
                im.save(f"{self.name}_{i}.jpg")
                text = pytesseract.image_to_string(Image.open(f"{self.name}_{i}.jpg"))
            else:
                text = pytesseract.image_to_string(im)

            text = text.strip()
            if debug:
                print(f"Detected({self.name}_{i}): {text}")

            if self.checkerFn(text):
                return True

        return False

class WaveGetter(Checker):
    def __init__(self, vp):
        super().__init__("WAVE", WAVE_OFFSET, vp, lambda t: "/" in t)

    def exec(self):
        for i in range(5):

            time.sleep(0.2)
            im = pyautogui.screenshot(region=self.offset)

            # enhance big spots
            im = im.filter(ImageFilter.MaxFilter(3))
            
            # threshold between text and background
            im = im.point(lambda p: 255 if p >= 255 else 0)

            # enhance text area
            im = im.filter(ImageFilter.MaxFilter(3))

            # gray scale
            im = im.convert("1")

            # remove noises
            im = im.filter(ImageFilter.MinFilter(3))

            # smooth out image
            im = im.filter(ImageFilter.SMOOTH)

            text = ""
            if debug:
                im.save(f"{self.name}_{i}.jpg")
                text = pytesseract.image_to_string(Image.open(f"{self.name}_{i}.jpg"))
            else:
                text = pytesseract.image_to_string(im)

            text = text.strip()
            if debug:
                print(f"Detected({self.name}_{i}): {text}")

            if self.checkerFn(text):
                return text

        return ""

class ScreenDebuger():
    def __init__(self, vp):
        self.builder = BuildChecker(vp)
        self.combater = CombatChecker(vp)
        self.ender = EndChecker(vp)
        self.retry = RetryChecker(vp)
        self.waver = WaveGetter(vp)
        self.menuer = MenuChecker(vp)

    def exec(self):
        self.builder.exec_debug()
        self.combater.exec_debug()
        self.ender.exec_debug()
        self.retry.exec_debug()
        self.waver.exec_debug()
        self.menuer.exec_debug()

class BuildChecker(Checker):
    def __init__(self, vp):
        super().__init__("BUILD", BUILD_OFFSET, vp, lambda t: any(map(t.__contains__, ["PRESS", "TO", "BEGIN"])))

class CombatChecker(Checker):
    def __init__(self, vp): 
        super().__init__("COMBAT", COMBAT_OFFSET, vp, lambda t: any(map(t.__contains__, ["PREPARE", "DEFENSE", "THEN", "PRESS", "WHEN", "READY"])))

class EndChecker(Checker):
    def __init__(self, vp):
        super().__init__("END", END_OFFSET, vp, lambda t: any(map(t.__contains__, ["PRESS", "TO", "MOVE", "ON"])))

class RetryChecker(Checker):
    def __init__(self, vp):
        super().__init__("RETRY", RETRY_OFFSET, vp, lambda t: any(map(t.__contains__, ["YES", "NO"])))

    def exec(self):
        for i in range(5):

            time.sleep(0.2)
            im = pyautogui.screenshot(region=self.offset)
            
            im = im.filter(ImageFilter.EDGE_ENHANCE)
            
            # threshold between text and background
            im = im.point(lambda p: 255 if p > 155 else 0)

            text = ""
            if debug:
                im.save(f"{self.name}_{i}.jpg")
                text = pytesseract.image_to_string(Image.open(f"{self.name}_{i}.jpg"))
            else:
                text = pytesseract.image_to_string(im)

            text = text.strip()
            if debug:
                print(f"Detected({self.name}_{i}): {text}")

            if self.checkerFn(text):
                return True

        return False

class MenuChecker(Checker):
    def __init__(self, vp):
        super().__init__("MENU", MENU_OFFSET, vp, lambda t: ("Replay") in t)

    def exec(self):
        for i in range(5):

            time.sleep(0.2)
            im = pyautogui.screenshot(region=self.offset)
            
            # enhance different between text and background
            enhancer = ImageEnhance.Contrast(im)
            im = enhancer.enhance(3)

            # to gray scale
            im = im.convert("1")
            text = ""
            if debug:
                im.save(f"{self.name}_{i}.jpg")
                text = pytesseract.image_to_string(Image.open(f"{self.name}_{i}.jpg"))
            else:
                text = pytesseract.image_to_string(im)

            text = text.strip()
            if debug:
                print(f"Detected({self.name}_{i}): {text}")

            if self.checkerFn(text):
                return True

        return False

    def get_replay_button(self):
        x, y, w, h = self.offset
        c_x = int(x + (w/2))
        c_y = int(y + (h/2) + (CURSOR_HEIGHT * self.scale))
        c_xy = (c_x, c_y)
        if debug:
            print(f"Replay Button: {c_xy}")
        return c_xy
