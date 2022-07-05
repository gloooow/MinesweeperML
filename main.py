import pyautogui
import random

base = 'img/'
img = {'cell':'cell.png', 
        'happy':'happy.png', 
        'sad':'sad.png',
        }

cell_number = len(list(pyautogui.locateAllOnScreen(base + img['cell'])))
random_cell = random.randrange(0, cell_number)


while(True):
    cell_list = list(pyautogui.locateAllOnScreen(base + img['cell']))
    cell_number = len(cell_list)
    random_cell = random.randrange(0, cell_number)
    
    pyautogui.click(cell_list[random_cell])
    if(pyautogui.locateOnScreen(base + img['sad'])):
        pyautogui.click(base + img['sad'])