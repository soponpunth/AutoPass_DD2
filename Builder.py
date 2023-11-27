import pyautogui
import time
from KeyMapping import *

N_MOVEMENTS = [W, A, S, D]
S_MOVEMENTS = [w, a, s, d]
N_SKILLS = [N1, N2, N3, N4, N5, N6, N7, N8]
K_SKILLS = [K1, K2, K3, K4, K5, K6, K7, K8]
SWITCH_HEROES = [F1, F2, F3, F4]

class Builder():

    def __init__(self):
        self.actions = []
        self.parse()

    def parse(self):
        from Combat import combats

        for c in combats:
            self.actions.append(c)

    def auto_build(self):
        return len(self.actions) > 0

    def exec(self):
        time.sleep(1)
        for action in self.actions:
            if action in N_MOVEMENTS:
                pyautogui.keyDown(action.lower())
                time.sleep(0.5)
                pyautogui.keyUp(action.lower())

            elif action in S_MOVEMENTS:
                pyautogui.keyDown(action)
                time.sleep(0.1)
                pyautogui.keyUp(action)

            elif action == J:
                pyautogui.press("space")

            elif action == Z or action == Q or action in N_SKILLS:
                pyautogui.press(action)
                time.sleep(0.1)
                pyautogui.click()
                time.sleep(0.1)
                pyautogui.press(action)

            elif action in K_SKILLS:
                pyautogui.press(action[0])
                time.sleep(0.1)
                pyautogui.click()
                time.sleep(0.1)
                pyautogui.click()
                time.sleep(0.1)
                pyautogui.press(action[0])

            elif action in SWITCH_HEROES:
                pyautogui.press(action)
                time.sleep(0.3)
