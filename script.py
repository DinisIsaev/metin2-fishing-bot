import mouse
import cv2
import numpy as np
from mss import mss
from PIL import ImageGrab

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
    lower = np.array([14, 87, 116])
    upper = np.array([19, 142, 128])
    #Filter all other colors
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    masked = cv2.bitwise_and(img, img, mask=mask)
    #Only show fish inside area
    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.circle(mask, (124, 97), 50, 255, -1)
    masked = cv2.bitwise_and(masked, masked, mask=mask)
    #Testing part to see image processing
    cv2.imshow('screen', masked)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
