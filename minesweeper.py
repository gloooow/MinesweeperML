import numpy as np
import cv2
import pyautogui
from PIL import ImageGrab, Image
import time

class Minesweeper:
    def __init__(self):
        self.cornerPixel = {'x': 16, 'y': 102}
        self.midPiel = {'x': 23, 'y': 109}
        self.cornerDistance = 16
        self.matrix = np.zeros((8, 8), dtype=object)
        self.base = 'img/'

        self.cells = {
            1: { # one - blue
                'corner': [192, 192, 192],
                'mid': [255, 0, 0],
                'value': 1,
            },
            2: { # two - green
                'corner': [192, 192, 192],
                'mid': [0, 128, 0],
                'value': 2,
            },
            3: { # three - red
                'corner': [192, 192, 192],
                'mid': [0, 0, 255],
                'value': 3,
            },
            4: { # four - purple
                'corner': [192, 192, 192],
                'mid': [128, 0, 0],
                'value': 4,
            },
            5: { # five - dark red
                'corner': [192, 192, 192],
                'mid': [0, 0, 128],
                'value': 5,
            },
            -1: { # empty cell
                'corner': [192, 192, 192],
                'mid': [192, 192, 192],
                'value': -1,
            },
            0: { # cell
                'corner': [255, 255, 255],
                'mid': [192, 192, 192],
                'value': 0,
            },
        }

    def take_screen_shot(self):
        return cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0,0,146,231))), cv2.COLOR_BGR2RGB)

    def identify_cell(self, image):
        currentMouseX_corner, currentMouseY_corner, currentMouseX_mid, currentMouseY_mid = 0, 0, 0, 0
        for i in range(8):
            for j in range(8):
                currentMouseX_corner = 16 + (i * 16)
                currentMouseY_corner = 102 + (j * 16)
                currentMouseX_mid = 23 + (i * 16)
                currentMouseY_mid = 109 + (j * 16)
                cornerPixel = image[currentMouseY_corner][currentMouseX_corner]
                midPixel = image[currentMouseY_mid][currentMouseX_mid]
                for(key, value) in self.cells.items():
                    if((cornerPixel == value['corner']).all() and (midPixel == value['mid']).all()):
                        self.matrix[j][i] = value['value']
                        break
                
    def main(self):
        image = self.take_screen_shot()
        self.identify_cell(image)

        print(self.matrix)


if __name__ == '__main__':
    minesweeper = Minesweeper()
    minesweeper.main()


# ML care sa invete ca trebuie sa apese doar pe 0
# inainte sa apese pe celula 0, sa se uite in jurul ei si sa vada daca e o idee buna sa apese acolo sau nu
# daca nu e idee buna, pune steag
# trb sa vad algoritm prin care sa determine daca e o idee buna sa apese pe 0 sau nu
# adica cumva trebuie sa stie ca daca are anumite chestii in jur, sa nu apese pe 0 ci sa puna steag
