import numpy as np
from PIL import ImageGrab
import time
import cv2
import pyautogui

now = time.time()

while(True):
    prtscr = np.array(ImageGrab.grab(bbox=(0,0,160,250), ))
    threshold = .9

    cell_template = cv2.imread('img/cell.png')
    cell_w, cell_h = cell_template.shape[:-1]
    cell_res = cv2.matchTemplate(prtscr, cell_template, cv2.TM_CCOEFF_NORMED)
    cell_loc = np.where(cell_res >= threshold)
    for pt in zip(*cell_loc[::-1]):  # Switch collumns and rows
        cv2.rectangle(prtscr, pt, (pt[0] + cell_w, pt[1] + cell_h), (0, 0, 0), 1)

    empty_template = cv2.imread('img/empty.png')
    empty_w, empty_h = empty_template.shape[:-1]
    empty_res = cv2.matchTemplate(prtscr, empty_template, cv2.TM_CCOEFF_NORMED)
    empty_loc = np.where(empty_res >= threshold)
    for pt in zip(*empty_loc[::-1]):  # Switch collumns and rows
        cv2.rectangle(prtscr, pt, (pt[0] + empty_w, pt[1] + empty_h), (0, 255, 255), 1)
    
    empty_down_template = cv2.imread('img/empty_down.png')
    empty_down_w, empty_down_h = empty_down_template.shape[:-1]
    empty_down_res = cv2.matchTemplate(prtscr, empty_down_template, cv2.TM_CCOEFF_NORMED)
    empty_down_loc = np.where(empty_down_res >= threshold)
    for pt in zip(*empty_down_loc[::-1]):  # Switch collumns and rows
        cv2.rectangle(prtscr, pt, (pt[0] + empty_down_w, pt[1] + empty_down_h), (0, 255, 255), 1)

    one_template = cv2.imread('img/1.png')
    one_template = cv2.cvtColor(one_template, cv2.COLOR_BGR2RGB)
    one_w, one_h = one_template.shape[:-1]
    one_res = cv2.matchTemplate(prtscr, one_template, cv2.TM_CCOEFF_NORMED)
    one_loc = np.where(one_res >= threshold)
    for pt in zip(*one_loc[::-1]):  # Switch collumns and rows
        cv2.rectangle(prtscr, pt, (pt[0] + one_w, pt[1] + one_h), (0, 0, 255), 3)

    two_template = cv2.imread('img/2.png')
    two_template = cv2.cvtColor(two_template, cv2.COLOR_BGR2RGB)
    two_w, two_h = two_template.shape[:-1]
    two_res = cv2.matchTemplate(prtscr, two_template, cv2.TM_CCOEFF_NORMED)
    two_loc = np.where(two_res >= threshold)
    for pt in zip(*two_loc[::-1]):  # Switch collumns and rows
        cv2.rectangle(prtscr, pt, (pt[0] + two_w, pt[1] + two_h), (0, 255, 0), 1)

    three_template = cv2.imread('img/3.png')
    three_template = cv2.cvtColor(three_template, cv2.COLOR_BGR2RGB)
    three_w, three_h = three_template.shape[:-1]
    three_res = cv2.matchTemplate(prtscr, three_template, cv2.TM_CCOEFF_NORMED)
    three_loc = np.where(three_res >= threshold)
    for pt in zip(*three_loc[::-1]):  # Switch collumns and rows
        cv2.rectangle(prtscr, pt, (pt[0] + three_w, pt[1] + three_h), (255, 0, 0), 1)

    cv2.imwrite('result.png', prtscr)


    # print('Loop took {} seconds'.format(time.time()-now))
    now = time.time()
    cv2.imshow('window',cv2.cvtColor(prtscr, cv2.COLOR_BGR2RGB))
    # cv2.imshow('window',prtscr)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
