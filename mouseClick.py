"""
This is just a helper file to get the points from the image for calculating homography
"""

# Recorded points:
#   Bottom Middle #1: (508, 897) -> ROBOT: (219, -1153, -171, -177, -3, 2)
#   Bottom Middle #2: (617, 899) -> ROBOT: (570, -1079, -176, 178, -9, 0)
#   Bottom Right #3: (1083, 1080) -> Robot: (742, -466, -164, 1787, -4, -4)
#   Top Right #3: (1094, 524) -> ROBOT: (172, -455, -165, -177, -4, -3)
#   (707, 1104) -> ROBOT:(781, -954, -170, -179, -9, 0)
#   (881, 818) -> ROBOT: (469, -720, -169, -179, -4, -4)
#   (687, 524) -> ROBOT: (190, -875, -175, -179, -8, 0)
#   (897, 506) -> ROBOT: (162, -698, -171, -175, -11, -4)
#   (1100, 669) -> ROBOT: (313, -435, -166, -177, -4, -4)

# Bunsen's Line should be at 800 px on the x axis

import cv2
from image_capture_demo import main

main()

# Load the image
image = cv2.imread('dice.png')
# image = cv2.imread('./diceImages/Problematic/dice1.png')
# image = cv2.resize(image, (0, 0), fx=0.2, fy=0.2)
image = cv2.resize(image, (1200, 1200))

# List to store clicked points
clicked_points = []

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Log the click position
        print(f"[{x}, {y}]")
        clicked_points.append((x, y))
        # Draw a small circle at the click position
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Calibration Image", image)

# Set up window and bind the mouse callback
cv2.imshow("Calibration Image", image)
cv2.setMouseCallback("Calibration Image", mouse_callback)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Recorded points:", clicked_points)
