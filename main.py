import numpy as np
from PIL import ImageGrab
import time
import cv2
import keyboard
import pyautogui

class Minesweeper:
    def __init__(self):
        self.base = 'img/'

        self.cells = {
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
                'first': '4.png',
                'second': (255, 0, 0),
                'third': 4,
            },
            5: {
                'first': '5.png',
                'second': (255, 0, 0),
                'third': 5,
            },
            6: {
                'first': 'cell.png',
                'second': (0, 0, 0),
                'third': 0,
            },
            7: {
                'first': 'empty_down.png',
                'second': (0, 255, 255),
                'third': -1,
            },
            8: {
                'first': 'empty.png',
                'second': (0, 255, 255),
                'third': -1,
            },
            9: {
                'first': 'empty_right.png',
                'second': (0, 255, 255),
                'third': -1,
            },
            10: {
                'first': 'empty_corner.png',
                'second': (0, 255, 255),
                'third': -1,
            },
            11: {
                'first': 'happy.png',
                'second': (0, 255, 255),
                'third': '9'
            },
            12: {
                'first': 'sad.png',
                'second': (255, 0, 255),
                'third': '-9'
            },
        }
        self.matrix = np.zeros((8, 8), dtype=object)
        self.ok = True
        self.reset_point = (0, 0)
        self.cursorPosition_x = 0
        self.cursorPosition_y = 0
        self.score = 0
        self.game_over = False
        self.main()

    def count_score(self, the_matrix):
        score = 0
        for row in the_matrix:
            for cell in row:
                if(cell['first'] == 0):
                    score += 1
        return score

    def map_cells_to_matrix(self, point, value):
        x, y = point
        interpolated_x = np.interp(x, [10,122], [0,7])
        interpolated_y = np.interp(y, [53,165], [0,7])
        self.matrix[round(interpolated_y)][round(interpolated_x)] = {'first': value, 'second': (x + 3, y + 3), 'third': (round(interpolated_x), round(interpolated_y))}
        # print("x: {}, y: {}, x_i: {}, y_i: {}, val: {}".format(x, y, interpolated_x, interpolated_y, value))

    def take_screen_shot(self):
        screen = np.array(ImageGrab.grab(bbox=(6,49,146,231)))
        return screen

    def reset_game(self):
        pyautogui.click(self.reset_point[0] + 10, self.reset_point[1] + 53)
        self.ok = True

    def process_img(self, original_image):
        processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        for number in self.cells.values():
            template = cv2.imread(self.base + number['first'])
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
                    self.map_cells_to_matrix((pt), number['third'])
                elif(number['first'] == 'happy.png'):
                    self.game_over = False
                elif(number['first'] == 'sad.png'):
                    # self.score = 0
                    self.reset_point = pt
                    self.game_over = True
                    # self.reset_game()
        return processed_img

    def move_cursor(self, direction):
        saved_score = self.score
        reward = 0
        check_game_over = False
        if direction == [1, 0, 0, 0, 0]:
            if(self.cursorPosition_x > 0):
                self.cursorPosition_x -= 1
                pyautogui.moveTo(self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][0] + 10, self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][1] + 53)
        elif direction == [0, 1, 0, 0, 0]:
            if(self.cursorPosition_y > 0):
                self.cursorPosition_y -= 1
                pyautogui.moveTo(self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][0] + 10, self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][1] + 53)
        elif direction == [0, 0, 1, 0, 0]:
            if(self.cursorPosition_x < 7):
                self.cursorPosition_x += 1
                pyautogui.moveTo(self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][0] + 10, self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][1] + 53)
        elif direction == [0, 0, 0, 1, 0]:
            if(self.cursorPosition_y < 7):
                self.cursorPosition_y += 1
                pyautogui.moveTo(self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][0] + 10, self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][1] + 53)
        elif direction == [0, 0, 0, 0, 1]:
            pyautogui.click()
            check_game_over = self.game_over == True
            if(check_game_over):
                reward = -20
                print('game over')
                saved_score = self.score
                self.score = 0
                self.reset_game()
            elif(self.matrix[self.cursorPosition_x][self.cursorPosition_y]['first'] == 0):
                self.score = 64 - self.count_score(self.matrix)
                saved_score = self.score
                print('good choice | {} | x: {} | y:{}'.format(self.matrix[self.cursorPosition_x][self.cursorPosition_y]['first'], self.cursorPosition_x, self.cursorPosition_y))
                reward = 10
        # print('Reward: {} | Score: {}'.format(reward, self.score))
        # print('Score: {}'.format(saved_score))
        return reward, check_game_over, saved_score

    def main(self):
        # while(True):
        screen = self.take_screen_shot()
        new_screen = self.process_img(screen)
        # print('Loop took {} seconds'.format(time.time()-last_time))
        if(self.ok):
            try:
                pyautogui.moveTo(self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][0] + 10, self.matrix[self.cursorPosition_x][self.cursorPosition_y]['second'][1] + 53)
            except:
                pyautogui.moveTo(10, 53)
                self.cursorPosition_x = 0
                self.cursorPosition_y = 0
            self.ok = False
        cv2.imshow('window', new_screen)   
        
