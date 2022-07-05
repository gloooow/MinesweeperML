from tempfile import TemporaryFile
import pyautogui

base = 'img/'
img = {'cell':'cell.png', 
        'happy':'happy.png', 
        'sad':'sad.png',
        }

minesweeperScreenshot = pyautogui.screenshot()
while(True):
    if(pyautogui.locateOnScreen(base + img['happy'])):
        pyautogui.click(base+img['cell'])
    else:
        pyautogui.click(base+img['sad'])
        pyautogui.moveTo(100,100)
