# AutoPass_DD2
 An automate script to press G v1.3...

## Prerequisite

1. [Python >= 3.8](https://www.python.org/downloads/windows/)
2. [PIP](https://pip.pypa.io/en/stable/installation/)
3. [tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

### Package from PIP
1. [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
2. [pytesseract](https://pypi.org/project/pytesseract/)

# Installation Guide
1. `pip install pyautogui pytesseract`
2. Edit `tesseract_path` in `Config.py` to your installed location

# What to expect
- Press `G` at the end of each wave except the first build phase.
- Once the run is done, there will be a **beep** sound to notify the player.
- If a wave is failed, a retry will automatically happen with a **beep** sound.

# Usage
1. Run the **DD2** game in a **Fullscreen Windowed** mode
2. Run `python AutoPass.py` when you are ready to combat!
3. (Optional, Only if auto_detect_wave=False) Enter a total number of remaining waves from the map

```
User> python AutoPass.py

```

# Config
```
# Path to tesseract
tesseract_path = "C:\\Path\\tesseract.exe"

# Automatically set a number of waves
# Set to False to input a number manually
auto_detect_wave = True

# Automatically click a replay button
# Set to True to enable the feature
auto_replay_map = False

# Beep sound duration in milliseconds
sound_ms = 1500

# Beep sound frequency range
sound_hz = 440

# Idle time before checking for the G button
# Increase this number as necessary when running Chaos 7+ maps
# DO NOT DECREASE BELOW 60 SECONDS !!!
wave_time_s = 70

# Set to True to enable more logging
debug = False
```

#### TODO
- Auto Build (difficulty 5/5)
