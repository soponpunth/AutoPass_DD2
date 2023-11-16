# AutoPass_DD2
 An automate script to press G v1.0...

## Prerequisite

1. [Python >= 3.8](https://www.python.org/downloads/windows/)
2. [PIP](https://pip.pypa.io/en/stable/installation/)
3. [tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

### Package from PIP
1. [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
2. [pytesseract](https://pypi.org/project/pytesseract/)

# Installation Guide
1. `pip install pyautogui`
2. `pip install pytesseract`
3. Edit `pytesseract.pytesseract.tesseract_cmd` to your installed location

# Usage
1. Run **DD2** game in **Fullscreen Windowed** mode
2. Run `python AutoPass.py`
3. Enter a number of waves for the map

```
User> python AutoPass.py
Screen  Size(width=3840, height=2160)
Enter number of waves:

```

#### TODO
- Auto Build (difficulty 5/5)
- Retry Wave (difficulty 2/5)
- Retry Map  (difficulty 2/5)