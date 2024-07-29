# metin2-test

Trying to automate fishing game task

Description:
In the game 'metin2' there's a fishing minigame, where you have to click a fish 3 times when the fish is in a specific area. I intend to automate this task using my knowledge in problem solving.

Challenges:

1. Detect fish
2. Detect when fish in area
3. Click on fish
4. Detect when a fish has been caught
5. Reput bait

Solutions:

1. Apply masks to highlight the fish in a cropped screenshot
2. Mask using a white circle the size of the area
3. Use win32api library for 'mouse' clicks
4. Check if fish exists in screen, even out of area; If not, we're not in the task
5. Use pydirectinput library for 'keyboard' press
6. Extra: I cut animation of pulling the rod by entering the mount and dismounting

Requirements:

1. Python 3.12

Packages:

1. numpy
2. cv2
3. pypiwin32
4. pydirectinput
5. mss
6. time

How to use:

1. Clone repo (duh)
2. Pip install all refered packages
3. Access cmd with admin privileges
4. Cd to this repo
5. Type .venv\Scripts\activate
6. Type py scripts.py
