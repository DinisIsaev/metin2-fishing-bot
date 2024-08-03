import win32api
import win32con
import cv2
import numpy as np
import time
import pydirectinput
from mss import mss
import os

#Drop function
def drop(screen, whatToDrop):
    res = cv2.matchTemplate(screen, whatToDrop, cv2.TM_CCOEFF_NORMED)
    if np.any(res > 0.9):
        items_location = np.where( res >= 0.9)
        for item in zip(*items_location):
            win32api.SetCursorPos((item[1]+1755, item[0]+740))
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            win32api.SetCursorPos((950, 565))
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            win32api.SetCursorPos((925, 565))
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
#Screens and image templates
minigame_box = {'top': 452, 'left': 837, 'width': 248, 'height': 197}
inventory_box = {'top': 725, 'left': 1750, 'width': 165, 'height': 290}
worm_box = {'top': 1044, 'left': 906, 'width': 32, 'height': 32}
sct = mss()
worm_template = cv2.imread("worm.png")
worm_template = cv2.cvtColor(np.array(worm_template), cv2.COLOR_BGR2RGB)
simbolo_template = cv2.imread("simbolo.png")
simbolo_template = cv2.cvtColor(np.array(simbolo_template), cv2.COLOR_BGR2RGB)
luva_template = cv2.imread("luva.png")
luva_template = cv2.cvtColor(np.array(luva_template), cv2.COLOR_BGR2RGB)
capa_template = cv2.imread("capa.png")
capa_template = cv2.cvtColor(np.array(capa_template), cv2.COLOR_BGR2RGB)
anel_template = cv2.imread("anel.png")
anel_template = cv2.cvtColor(np.array(anel_template), cv2.COLOR_BGR2RGB)
gold_ring_template = cv2.imread("gold_ring.png")
gold_ring_template = cv2.cvtColor(np.array(gold_ring_template), cv2.COLOR_BGR2RGB)

#Color masking bounds
lower = np.array([14, 87, 115])
upper = np.array([17, 157, 126])

while True:
    #Grab fish screen
    minigame_rec = sct.grab(minigame_box)
    minigame_rec = cv2.cvtColor(np.array(minigame_rec), cv2.COLOR_BGR2RGB) 
    #Filter out all other colors besides fish and only in the middle
    hsv = cv2.cvtColor(minigame_rec, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    masked = cv2.bitwise_and(minigame_rec, minigame_rec, mask=mask) 
    masked_save = masked.copy()
    mask = np.zeros(minigame_rec.shape[:2], dtype="uint8")
    cv2.circle(mask, (124, 97), 55, 255, -1)
    masked = cv2.bitwise_and(masked, masked, mask=mask)
    #Find coords for fish
    points = cv2.findNonZero(masked[:,:,0])
    #Press on coords
    if points is not None:
        worm = False
        win32api.SetCursorPos((points[0][0][0]+837, points[0][0][1]+452))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    #If finished minigame: reput bait and fish again
    elif cv2.findNonZero(masked_save[:,:,0]) is None:
        #Grab inventory screen
        inventory_rec = sct.grab(inventory_box)
        inventory_rec = cv2.cvtColor(np.array(inventory_rec), cv2.COLOR_BGR2RGB) 
        #Grab worm slot screen
        worm_slot_rec = sct.grab(worm_box)
        worm_slot_rec = cv2.cvtColor(np.array(worm_slot_rec), cv2.COLOR_BGR2RGB)
        #Check if there is a worm in slot
        res = cv2.matchTemplate(worm_slot_rec, worm_template, cv2.TM_CCOEFF_NORMED)
        #If no worm in slot search inventory for it
        if not np.any(res > 0.9):
            res = cv2.matchTemplate(inventory_rec, worm_template, cv2.TM_CCOEFF_NORMED)
            #If there are more worms, put on slot
            if np.any(res > 0.9):
                worm_location = np.where( res >= 0.9)
                worm = list(zip(*worm_location))
                if worm:
                    win32api.SetCursorPos((worm[0][1]+1755, worm[0][0]+740))
                    pydirectinput.keyDown("ctrl")
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    pydirectinput.keyUp("ctrl")
            #If there are no more worms to use stop code
            else:
                break 
        #Open fishes
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
        #Drop capes and stuff
        drop(inventory_rec, capa_template)
        drop(inventory_rec, anel_template)
        drop(inventory_rec, luva_template)
        drop(inventory_rec, simbolo_template)
        drop(inventory_rec, gold_ring_template)
        pydirectinput.keyDown("ctrl")
        pydirectinput.keyDown("g")
        pydirectinput.keyUp("g")
        pydirectinput.keyDown("g")
        pydirectinput.keyUp("g")
        pydirectinput.keyUp("ctrl")
        pydirectinput.keyDown('2')
        pydirectinput.keyUp('2')
        pydirectinput.keyDown('1')
        pydirectinput.keyUp('1')
    '''
    cv2.imshow("test", worm1_slot)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
    '''
