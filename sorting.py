# BUNSEN REACH: 
#   TOP:    [148, -1170]
#           [360, -1122]
#   BOTTOM: [584, -1074]
# 

# BEAKER REACH:
#   TOP:    [170, 1200]
#           [344, 1155]
#   BOTTOM: [564, 1066]

import cv2
import json
import diceDetection

# Other potential coordinate sort for bunsen, I believe this is a better method with the dynamic y coords
def getBunsenCoords():
    diceCoords = diceDetection.detectDice(False)
    coords = json.loads(diceCoords[0])
    print(coords)

    # Sort the coords list based on the y position. This gives a nice pickup from left to right
    sorted_coords = sorted(coords, key=lambda c: (c["pos"][1]), reverse=True)

    bunsen_coords = []

    for i, c in enumerate(sorted_coords, start=1):
        tmpCoord = c["pos"]
        bunsen_coords.append(tmpCoord)
        
    return bunsen_coords

def getBeakerCoords():
    diceCoords = diceDetection.detectDice(False)
    coords = json.loads(diceCoords[1])

    # Sort the coords list based on the y position. This gives a nice pickup from left to right
    sorted_coords = sorted(coords, key=lambda c: (c["pos"][1]), reverse=True)

    beaker_coords = []

    for i, c in enumerate(sorted_coords, start=1):
        tmpCoord = c["pos"]
        beaker_coords.append(tmpCoord)
        
    print(beaker_coords)
    return beaker_coords

"""

Unused function -- Not deleting until lab is finished incase the ideas are useful

# Get coordinates of the dice in the safe and exclusion zone for bunsen
def bunsenGetCoords():
    coords = json.loads(diceDetection.detectDice(False))

    # Sort the coords list based on the y position. This gives a nice pickup from left to right
    sorted_coords = sorted(coords, key=lambda c: (c["pos"][1]), reverse=True)

    bunsen_safe_coords = []
    bunsen_exclusion_coords = []
    # beaker_safe_coords = []
    # beaker_exclusion_coords = []

    bunsen_coord_package = []
    # beaker_coord_package = []

    # give only bunsen the dice from -1075 and to the right
    for i, c in enumerate(sorted_coords, start=1):
        tmpCoord = c["pos"]
        if (tmpCoord[1] > -1000):
            bunsen_safe_coords.append(tmpCoord)
        elif (tmpCoord[1] > -1075):
            bunsen_exclusion_coords.append(tmpCoord)
        # elif (tmpCoord[1] < -1300):
        #     beaker_safe_coords.append(tmpCoord)
        # else:
        #     beaker_exclusion_coords.append(tmpCoord)
        
    print("Bunsen_Safe_Coords:", bunsen_safe_coords)
    print("Bunsen_Exclusion_Coords:", bunsen_exclusion_coords)
    # print("Beaker_Safe_Coords:", beaker_safe_coords)
    # print("Beaker_Exclusion_Coords:", beaker_exclusion_coords)

    bunsen_coord_package.append(bunsen_safe_coords)
    bunsen_coord_package.append(bunsen_exclusion_coords)
    # beaker_coord_package.append(beaker_safe_coords)
    # beaker_coord_package.append(beaker_exclusion_coords)

    # if (isBunsen):
        # return bunsen_coord_package
    # else:
        # return beaker_coord_package
    return bunsen_coord_package
"""
    
if __name__ == '__main__':
    # testing
    getBeakerCoords()