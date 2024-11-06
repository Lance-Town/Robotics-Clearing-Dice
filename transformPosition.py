import nathan_dice_processing
import homography
import cv2
import json

        dice_info.append({
            'x': center_x,
            'y': center_y,
            'rot': angle,
            'pips': pip_count,
        })

    with open('dice_info.json', 'w') as json_file:
        json_file.write(dice_info_json)