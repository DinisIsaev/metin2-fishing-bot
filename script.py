import win32api
import win32con
import cv2
import numpy as np
import time
import pydirectinput
from mss import mss
import os

minigame_box = {'top': 452, 'left': 837, 'width': 248, 'height': 197}
inventory_box = {'top': 725, 'left': 1750, 'width': 165, 'height': 290}
worm_box = {'top': 1044, 'left': 906, 'width': 32, 'height': 32}
sct = mss()

while True:
    #Grab fish screen
    img = sct.grab(minigame_box)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB) 
    #Masking
    lower = np.array([14, 87, 115])
    upper = np.array([17, 157, 126])
    #Filter out all other colors besides fish
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    masked = cv2.bitwise_and(img, img, mask=mask) 
    masked_save = masked.copy()
    #Only show fish inside area
    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.circle(mask, (124, 97), 55, 255, -1)
    masked = cv2.bitwise_and(masked, masked, mask=mask)
    #Find coords
    points = cv2.findNonZero(masked[:,:,0])
    #Press on coords
    if points is not None:
        worm = False
        win32api.SetCursorPos((points[0][0][0]+837, points[0][0][1]+452))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    #If finished migame: reput bait and fish again
    elif cv2.findNonZero(masked_save[:,:,0]) is None:
        inventory_rec = sct.grab(inventory_box)
        inventory_rec = cv2.cvtColor(np.array(inventory_rec), cv2.COLOR_BGR2RGB) 
        worm_template = cv2.imread("worm.png")
        worm_template = cv2.cvtColor(np.array(worm_template), cv2.COLOR_BGR2RGB)
        worm_slot_rec = sct.grab(worm_box)
        worm_slot_rec = cv2.cvtColor(np.array(worm_slot_rec), cv2.COLOR_BGR2RGB)
        res = cv2.matchTemplate(worm_slot_rec, worm_template, cv2.TM_CCOEFF_NORMED)
        if not np.any(res > 0.9):
            res = cv2.matchTemplate(inventory_rec, worm_template, cv2.TM_CCOEFF_NORMED)
            if np.any(res > 0.9):
                worm_location = np.where( res >= 0.9)
                for worm in zip(*worm_location):
                    win32api.SetCursorPos((worm[1]+1755, worm[0]+740))
                    pydirectinput.keyDown("ctrl")
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    pydirectinput.keyUp("ctrl")
            else:
                break
        for i in range(16):
            file = str(i+1)+".png"
            fish_img = cv2.imread(file)
            fish_img = cv2.cvtColor(np.array(fish_img), cv2.COLOR_BGR2RGB) 
            res = cv2.matchTemplate(inventory_rec, fish_img, cv2.TM_CCOEFF_NORMED)
            if np.any(res > 0.9):
                fish_location = np.where( res >= 0.9)
                for fish in zip(*fish_location):
                    win32api.SetCursorPos((fish[1]+1755, fish[0]+740))
                    time.sleep(0.1)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        time.sleep(0.25)
        pydirectinput.keyDown("ctrl")
        pydirectinput.keyDown("g")
        pydirectinput.keyUp("g")
        time.sleep(0.25)
        pydirectinput.keyDown("g")
        pydirectinput.keyUp("g")
        pydirectinput.keyUp("ctrl")
        time.sleep(0.25)
        pydirectinput.keyDown('2')
        pydirectinput.keyUp('2')
        time.sleep(0.25)
        pydirectinput.keyDown('1')
        pydirectinput.keyUp('1')


    '''
    cv2.imshow("test", worm_slot)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
    '''