# Joseph Wang
# 1/12/2021
# Piano Tiles
# Automatically detects piano tiles and plays them from this website http://tanksw.com/piano-tiles/ under Rush mode

from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

# Tile 1 Position: X:  758 Y:  940 RGB: (249, 231,  23)
# Tile 2 Position: X:  890 Y:  940 RGB: (249, 231,  23)
# Tile 3 Position: X: 1005 Y:  940 RGB: (249, 231,  23)
# Tile 4 Position: X: 1140 Y:  940 RGB: (249, 231,  23)

# Black: RGB: (17, 17, 17)

y = 800

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

while keyboard.is_pressed('q') == False:
    print(pyautogui.pixel(758, y))
    if pyautogui.pixel(758, y)[0] == 17:
        click(758, y)
    if pyautogui.pixel(890, y)[0] == 17:
        click(890, y)
    if pyautogui.pixel(1005, y)[0] == 17:
        click(1005, y)
    if pyautogui.pixel(1140, y)[0] == 17:
        click(1140, y)