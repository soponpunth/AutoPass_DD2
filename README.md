# AutoPass_DD2
 An automate script to press G v1.2...

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
3. Enter a total number of remaining waves from the map

```
User> python AutoPass.py
Enter number of waves:

```

#### TODO
- Auto Build (difficulty 5/5)
- Retry Map  (difficulty 2/5)
- Auto Wave  (difficulty 3/5)