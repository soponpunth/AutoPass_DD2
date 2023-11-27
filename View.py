
import pyautogui
import time
from Config import wave_time_s
from enum import Enum
from Checker import BuildChecker, CombatChecker, EndChecker, RetryChecker, MenuChecker, WaveGetter


class Result(Enum):
    NONE = 0
    COMBAT = 1
    RETRY = 2
    MENU = 3
    BUILD = 4
    END = 5


class View():

    def __init__(self):
        self.waves = 0
        self.current_wave = 0
        self.viewport = self.get_viewport()

    def is_map_done(self):
        return self.waves > 0 and self.current_wave >= self.waves

    def read_number_of_waves(self):
        self.waves = int(input("Enter number of waves: "))
        self.current_wave = 0

    def update_wave(self):
        self.current_wave += 1

    def retry_wave(self):
        self.current_wave -= 1

    def get_viewport(self):
        return pyautogui.size()

    def display_start_map(self):
        print(f"Screen {self.viewport[0], self.viewport[1]}")
        print(f"Starting in...")
        for i in range(5, 0, -1):
            print(i)
            time.sleep(1)

    def idle(self):
        for i in range(wave_time_s):
            if i % 10 == 0:
                print(f"Waiting {i} / {wave_time_s} seconds")
            time.sleep(1)

    def display_current_wave(self):
        print(f"Running Wave: {self.current_wave} / {self.waves}")

    def check_for_combat_phase(self):
        combatChecker = CombatChecker(self.viewport)
        retryChecker = RetryChecker(self.viewport)

        for _ in range(30):
            if combatChecker.exec():
                return Result.COMBAT

            if retryChecker.exec():
                return Result.RETRY

            print(f"Waiting for next combat...")
            time.sleep(5)

        raise Exception(f"Failed to detect combat or retry phase during wave ({self.current_wave}/{self.waves})")

    def check_for_build_phase(self):
        buildChecker = BuildChecker(self.viewport)

        for _ in range(20):
            if buildChecker.exec():
                return Result.BUILD

            time.sleep(5)

        raise Exception(f"Failed to detect build phase during wave ({self.current_wave}/{self.waves})")

    def check_for_end_phase(self):
        endChecker = EndChecker(self.viewport)

        for _ in range(30):
            if endChecker.exec():
                return Result.END

            time.sleep(3)

        raise Exception(f"Failed to detect end phase during wave ({self.current_wave}/{self.waves})")

    def check_for_menu_phase(self):
        menuChecker = MenuChecker(self.viewport)
        for _ in range(5):
            if menuChecker.exec():
                return Result.MENU

            time.sleep(3)

        raise Exception(f"Failed to detect menu phase during wave ({self.current_wave}/{self.waves})")

    def check_for_wave_menu(self):
        waveGetter = WaveGetter(self.viewport)
        for _ in range(2):
            wave = waveGetter.exec()
            if wave:
                waveIdx = wave.find("/")
                self.waves = int(wave[waveIdx + 1])
                self.current_wave = int(wave[waveIdx - 1]) - 1
                return Result.NONE

            time.sleep(1)

        raise Exception(f"Failed to detect wave menu during wave ({self.current_wave}/{self.waves})")

    def click_retry_button(self):
        menuChecker = MenuChecker(self.viewport)
        x, y = menuChecker.get_replay_button()
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.click()
        # loading screen
        time.sleep(15)
        self.check_for_build_phase()
