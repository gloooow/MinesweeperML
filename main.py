import numpy as np
from PIL import ImageGrab
import time
import cv2
import pyautogui

base = 'img/'

cells = {
    1: {
        'first': '1.png',
        'second': (0, 0, 255),
    },
    2: {
        'first': '2.png',
        'second': (0, 255, 0),
    },
    3: {
        'first': '3.png',
        'second': (255, 0, 0),
    },
    4: {
        'first': 'cell.png',
        'second': (0, 0, 0),
    },
    5: {
        'first': 'empty_down.png',
        'second': (255, 255, 255),
    },
    6: {
        'first': 'empty.png',
        'second': (255, 255, 255),
    },
    7: {
        'first': 'empty_right.png',
        'second': (255, 255, 255),
    },
    8: {
        'first': 'empty_corner.png',
        'second': (255, 255, 255),
    },
    9: {
        'first': 'happy.png',
        'second': (0, 255, 255),
    },
    10: {
        'first': 'sad.png',
        'second': (255, 0, 255),
    },
}

def take_screen_shot():
    # 800x600 windowed mode
    screen = np.array(ImageGrab.grab(bbox=(0,0,150,250)))
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
    
    return processed_img

def main():
    last_time = time.time()
    while(True):
        screen = take_screen_shot()
        new_screen = process_img(screen)
        # print('Loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window', new_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()

