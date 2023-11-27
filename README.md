# AutoPass_DD2
 An automate script to press G v2.0...

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

# Debug flag for developing build sequence
# Set to True to enable the feature
debug_build = False
```

## Auto Build
1. Edit `combats` in `Combat.py` by using syntax below (leave empty to disable the feature)
```
# Combat Sequence
W = Move Forward
S = Move Backward
A = Move Left
D = Move Right
J = Jump
Z = Sell Defense
Q = Upgrade Defense
N1 = Skill slot 1
N2 = Skill slot 2
N3 = Skill slot 3
N4 = Skill slot 4
N5 = Skill slot 5
N6 = Skill slot 6
N7 = Skill slot 7
N8 = Skill slot 8
K1 = Skill slot 1 + Confirm
K2 = Skill slot 2 + Confirm
K3 = Skill slot 3 + Confirm
K4 = Skill slot 4 + Confirm
K5 = Skill slot 5 + Confirm
K6 = Skill slot 6 + Confirm
K7 = Skill slot 7 + Confirm
K8 = Skill slot 8 + Confirm
F1 = Switch to F1 hero slot
F2 = Switch to F2 hero slot
F3 = Switch to F3 hero slot
F4 = Switch to F4 hero slot

# Example
# Switch to F2 hero slot
# Move Forward
# Move Right
# Build Defense on key slot 6
# Move Backward
# Build Defense on key slot 7
combats = [F2, W, D, N6, S, N7]
```

Recommend to use **debug_build** to True to find a proper building sequence for the map.
When enabled, the program will only execute the combat sequence and exit. The actual combat phase will not start!
