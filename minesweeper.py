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
        self.matrix = np.zeros((10, 10), dtype=object)
        self.matrix_aux = np.zeros((10, 10), dtype=object)
        self.base = 'img/'

        self.x_directions = [-1,0,1,-1,1,-1,0,1]
        self.y_directions = [-1,-1,-1,0,0,1,1,1]

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
            'b': { # bomb
                'corner': [0, 0, 255],
                'mid': [0, 0, 0],
                'value': 'b',
            },
            'f': { # flag
                'corner': [255, 255, 255],
                'mid': [0, 0, 0],
                'value': 'f',
            },
        }
    def init_matrix_border(self):
        for i in range(10):
            self.matrix[0][i], self.matrix_aux[0][i] = 'o','o'
            self.matrix[9][i], self.matrix_aux[9][i] = 'o','o'
            self.matrix[i][0], self.matrix_aux[i][0] = 'o','o'
            self.matrix[i][9], self.matrix_aux[i][9] = 'o','o'
        
    def take_screen_shot(self):
        return cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0,0,146,231))), cv2.COLOR_BGR2RGB)

    def identify_cell(self, image):
        currentMouseX_corner, currentMouseY_corner, currentMouseX_mid, currentMouseY_mid = 0, 0, 0, 0
        for i in range(1, 9):
            for j in range(1, 9):
                currentMouseX_corner = 16 + ((i - 1) * 16)
                currentMouseY_corner = 102 + ((j - 1) * 16)
                currentMouseX_mid = 23 + ((i - 1) * 16)
                currentMouseY_mid = 109 + ((j - 1) * 16)
                cornerPixel = image[currentMouseY_corner][currentMouseX_corner]
                midPixel = image[currentMouseY_mid][currentMouseX_mid]
                for(key, value) in self.cells.items():
                    if((cornerPixel == value['corner']).all() and (midPixel == value['mid']).all()):
                        self.matrix[j][i] = value['value']
                        break
    def surely_flag(self):
        ok = False
        for i in range(1, 9):
            for j in range(1, 9):
                empty_cells = 0
                flag_coordinates = []
                for d in range(8):
                    dir_x = i + self.x_directions[d]
                    dir_y = j + self.y_directions[d]
                    if(self.matrix[i][j] != 0 and self.matrix[dir_x][dir_y] == 0):
                        empty_cells += 1
                        ok = True
                        flag_coordinates.append([dir_x, dir_y])
                if(empty_cells == self.matrix[i][j] and empty_cells != 0):
                    for flags in flag_coordinates:
                        if(self.matrix[flags[0]][flags[1]] == 0):
                            self.matrix_aux[flags[0]][flags[1]] = 'f'
        
        for i in range(1, 9):
            for j in range(1, 9):
                if(self.matrix_aux[i][j] == 'f'):
                        pyautogui.rightClick(self.cornerPixel['x'] + ((j - 1) * self.cornerDistance), self.cornerPixel['y'] + ((i - 1) * self.cornerDistance))
        return ok
        
    def transfer_flag_matrix(self):
        for i in range(1, 9):
            for j in range(1, 9):
                if(self.matrix_aux[i][j] == 'f'):
                    self.matrix[i][j] = 'f'
                    self.matrix_aux[i][j] = 0
    def main(self):
        self.init_matrix_border()
        while(True):
            image = self.take_screen_shot()
            self.identify_cell(image)
            self.surely_flag()
            self.transfer_flag_matrix()
            break

if __name__ == '__main__':
    minesweeper = Minesweeper()
    start_time = time.time()
    minesweeper.main()
    print("--- %s seconds ---" % (time.time() - start_time))


# ML care sa invete ca trebuie sa apese doar pe 0
# inainte sa apese pe celula 0, sa se uite in jurul ei si sa vada daca e o idee buna sa apese acolo sau nu
# daca nu e idee buna, pune steag
# trb sa vad algoritm prin care sa determine daca e o idee buna sa apese pe 0 sau nu
# adica cumva trebuie sa stie ca daca are anumite chestii in jur, sa nu apese pe 0 ci sa puna steag
