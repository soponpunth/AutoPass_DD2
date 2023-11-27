#!/usr/bin/env python

import winsound
import pyautogui
from View import View, Result
from Config import sound_ms, sound_hz, auto_detect_wave, auto_replay_map

def main_control(view):
    if not auto_detect_wave:
        view.read_number_of_waves()
    
    view.display_start_map()
    
    if auto_detect_wave:
        view.check_for_wave_menu()

    while not view.is_map_done():
        result = view.check_for_combat_phase()
        if result == Result.COMBAT:
            # press G to start combat phase
            pyautogui.press("g")
            view.update_wave()
            view.display_current_wave()
            view.idle()
        elif result == Result.RETRY:
            # press Y to retry
            pyautogui.press("y")
            # loading screen should happen here
            winsound.Beep(sound_hz, sound_ms)
            view.check_for_build_phase()
            # press G to start build phase
            pyautogui.press("g")
            view.retry_wave()

    view.check_for_end_phase()
    # press G to move on
    pyautogui.press("g")
    view.check_for_menu_phase()

    if auto_replay_map:
        view.click_retry_button()

    # the run is done
    winsound.Beep(sound_hz, sound_ms)

if __name__ == "__main__":

    view = View()
    main_control(view)