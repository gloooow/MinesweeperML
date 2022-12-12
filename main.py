import numpy as np
from PIL import ImageGrab
import time
import cv2
import keyboard
import pyautogui

base = 'img/'

cells = {
    1: {
        'first': '1.png',
        'second': (0, 0, 255),
        'third': 1,
    },
    2: {
        'first': '2.png',
        'second': (0, 255, 0),
        'third': 2,
    },
    3: {
        'first': '3.png',
        'second': (255, 0, 0),
        'third': 3,
    },
    4: {
        'first': 'cell.png',
        'second': (0, 0, 0),
        'third': 0,
    },
    5: {
        'first': 'empty_down.png',
        'second': (0, 255, 255),
        'third': -1,
    },
    6: {
        'first': 'empty.png',
        'second': (0, 255, 255),
        'third': -1,
    },
    7: {
        'first': 'empty_right.png',
        'second': (0, 255, 255),
        'third': -1,
    },
    8: {
        'first': 'empty_corner.png',
        'second': (0, 255, 255),
        'third': -1,
    },
    9: {
        'first': 'happy.png',
        'second': (0, 255, 255),
        'third': '9'
    },
    10: {
        'first': 'sad.png',
        'second': (255, 0, 255),
        'third': '-9'
    },
}

matrix = np.zeros((8, 8), dtype=object)

def map_cells_to_matrix(point, value):
    x, y = point
    interpolated_x = np.interp(x, [10,122], [0,7])
    interpolated_y = np.interp(y, [53,165], [0,7])
    matrix[round(interpolated_y)][round(interpolated_x)] = {'first': value, 'second': (x + 7, y  + 7), 'third': (round(interpolated_x), round(interpolated_y))}
    # print("x: {}, y: {}, x_i: {}, y_i: {}, val: {}".format(x, y, interpolated_x, interpolated_y, value))

def take_screen_shot():
    screen = np.array(ImageGrab.grab(bbox=(6,49,146,231)))
    return screen

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    for number in cells.values():
        template = cv2.imread(base + number['first'])
        w, h = template.shape[:-1]
        res = cv2.matchTemplate(processed_img,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            xOffset, yOffset = 0, 0
            if(number['first'] == 'cell.png' or number['first'] == 'empty.png' or number['first'] == 'empty_corner.png' or number['first'] == 'empty_down.png' or number['first'] == 'empty_right.png'):
                xOffset, yOffset = 1, 1
            cv2.rectangle(processed_img, (pt[0] + xOffset, pt[1] + yOffset), (pt[0] + w - xOffset - 1, pt[1] + h - yOffset - 1), number['second'])
            if(number['first'] != 'happy.png' and number['first'] != 'sad.png'):
                map_cells_to_matrix((pt), number['third'])
    return processed_img


def main():
    last_time = time.time()
    ok = True
    while(True):
        screen = take_screen_shot()
        new_screen = process_img(screen)
        # print('Loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        if(ok):
            cursorPosition_x = 0
            cursorPosition_y = 0
            pyautogui.moveTo(matrix[cursorPosition_x][cursorPosition_y]['second'][0] + 10, matrix[cursorPosition_x][cursorPosition_y]['second'][1] + 53)
            ok = False
        cv2.imshow('window', new_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
        if keyboard.is_pressed('w'):
            if(cursorPosition_x > 0):
                cursorPosition_x -= 1
                pyautogui.moveTo(matrix[cursorPosition_x][cursorPosition_y]['second'][0] + 10, matrix[cursorPosition_x][cursorPosition_y]['second'][1] + 53)
        elif keyboard.is_pressed('a'):
            if(cursorPosition_y > 0):
                cursorPosition_y -= 1
                pyautogui.moveTo(matrix[cursorPosition_x][cursorPosition_y]['second'][0] + 10, matrix[cursorPosition_x][cursorPosition_y]['second'][1] + 53)
        elif keyboard.is_pressed('s'):
            if(cursorPosition_x < 7):
                cursorPosition_x += 1
                pyautogui.moveTo(matrix[cursorPosition_x][cursorPosition_y]['second'][0] + 10, matrix[cursorPosition_x][cursorPosition_y]['second'][1] + 53)
        elif keyboard.is_pressed('d'):
            if(cursorPosition_y < 7):
                cursorPosition_y += 1
                pyautogui.moveTo(matrix[cursorPosition_x][cursorPosition_y]['second'][0] + 10, matrix[cursorPosition_x][cursorPosition_y]['second'][1] + 53)
        elif keyboard.is_pressed('space'):
            pyautogui.click()

if __name__ == '__main__':
    main()
