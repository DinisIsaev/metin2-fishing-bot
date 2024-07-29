import win32api
import win32con
import time
import cv2
import numpy as np
import pydirectinput
from mss import mss

'''
while True:
    screen = ImageGrab.grab()
    screen.save("screenshot.png")
    img = cv2.imread('screenshot.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    cv2.imshow("test", img[452:645,837:1085])
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
'''
bounding_box = {'top': 452, 'left': 837, 'width': 248, 'height': 197}

sct = mss()

while True:
    #Grab fish screen
    img = sct.grab(bounding_box)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB) 

    #Masking
    lower = np.array([14, 87, 115])
    upper = np.array([17, 157, 126])
    #Filter all other colors
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    masked = cv2.bitwise_and(img, img, mask=mask)
    masked_save = masked.copy()
    #Only show fish inside area
    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.circle(mask, (124, 97), 60, 255, -1)
    masked = cv2.bitwise_and(masked, masked, mask=mask)
    #Find coords
    points = cv2.findNonZero(masked[:,:,0])
    #Press on coords
    if points is not None:
        win32api.SetCursorPos((points[0][0][0]+837, points[0][0][1]+452))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    elif points is None and cv2.findNonZero(masked_save[:,:,0]) is None:
        pydirectinput.keyDown('ctrl')
        pydirectinput.keyDown('g')
        pydirectinput.keyUp('g')
        pydirectinput.keyDown('g')
        pydirectinput.keyUp('g')
        pydirectinput.keyUp('ctrl')
        pydirectinput.keyDown('2')
        pydirectinput.keyUp('2')
        pydirectinput.keyDown('1')
        pydirectinput.keyUp('1')
    #Testing part to see image processing
    cv2.imshow('screen', masked_save)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break