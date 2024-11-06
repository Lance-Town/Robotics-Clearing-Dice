import numpy as np
import cv2

"""
Using Lance Image processing with 1200 by 1200 -- Works
# New image points since someone kicked the camera
bunsen_image_points_1 = np.array([
    [786, 525],
    [783, 818],
    [771, 1077],
    [942, 1094], # possibly crooked bottom middle
    [948, 826],
    [963, 521],
    [1124, 521],
    [1109, 816],
    [1082, 1119]
], dtype="float32")

# New robot points since someone kicked the camera
bunsen_robot_points_1 = np.array([
    [175, -841],
    [477, -838],
    [738, -849],
    [749, -615], # Possibly crooked bottom middle 
    [474, -623],
    [177, -606],
    [170, -406],
    [448, -402],
    [769, -433]
], dtype="float32")
"""

"""
# Using Nathans image processing points -- WITHOUT THE 0.2 SCALING -- NORMAL POSITIONS
bunsen_image_points = np.array([
    [2610, 2784],
    [3621, 2111],
    [3667, 1379],
    [3074, 1374],
    [3051, 2121],
    [3026, 2786],
    [2497, 2753],
    [2493, 2118],
    [2511, 1372]
], dtype="float32")

#  Robot points for Nathans image processing points
bunsen_robot_points = np.array([
    [747, -437],
    [472, -437],
    [186, -437],
    [186, -662],
    [482, -662],
    [755, -662],
    [755, -881],
    [496, -881],
    [199, -881]

], dtype="float32")

# These are image points using nathans scaling -- WITH THE 0.2x SCALING -- I believe
# These correspoind with the beaker_robot_points below, near line 89
beaker_image_points = np.array([
    [192, 1412],
    [208, 2038],
    [219, 2721],
    [827, 2739],
    [821, 2022],
    [832, 1459],
    [1427, 1468],
    [1420, 2103],
    [1350, 2764]
], dtype="float32")

# # These are image points using my scaling of (1200, 1200).
# # These correspoind with the beaker_robot_points directly below
# beaker_image_points = np.array([
#     [56, 560],
#     [59, 808],
#     [62, 1080],
#     [247, 1087],
#     [244, 801],
#     [247, 577],
#     [423, 579],
#     [422, 833],
#     [404, 1096]
# ], dtype="float32")


beaker_robot_points = np.array([
    [213, 449],
    [474, 449],
    [768, 449],
    [764, 716],
    [466, 716],
    [225, 723],
    [225, 973],
    [485, 969],
    [765, 937]
], dtype="float32")

"""

"""
# These are image points using nathans scaling -- WITH THE 0.2x SCALING -- I believe
# These correspoind with the beaker_robot_points below, near line 89
# THESE ARE OKAY -- ONLY BUNSEN NEEDS TO CHANGE -- Nevermind, not using these. 1200 x 1200 works well
beaker_image_points = np.array([
    [20, 275],
    [25, 414],
    [25, 518],
    [141, 523],
    [139, 429],
    [137, 293],
    [257, 296],
    [258, 417],
    [257, 525]
], dtype="float32")

beaker_robot_points = np.array([
    [197, 414],
    [487, 414],
    [708, 414],
    [708, 662],
    [510, 662],
    [230, 662],
    [243, 911],
    [485, 911],
    [723, 911]
], dtype="float32")
"""

# These are image points using Lance's scaling of (1200, 1200).
# These correspoind with the beaker_robot_points directly below
# THESE BOTH WORK. JUST KEEP EM. I AM HAPPY
beaker_image_points_2 = np.array([
    [56, 560],
    [59, 808],
    [62, 1080],
    [247, 1087],
    [244, 801],
    [247, 577],
    [423, 579],
    [422, 833],
    [404, 1096]
], dtype="float32")


beaker_robot_points_2 = np.array([
    [213, 449],
    [474, 449],
    [768, 449],
    [764, 716],
    [466, 716],
    [225, 723],
    [225, 973],
    [485, 969],
    [765, 937]
], dtype="float32")

# Using Lance Image processing with 1200 by 1200 -- Works. Thankfully. I am done lol
# New image points since someone kicked the camera
bunsen_image_points_1 = np.array([
    [786, 525],
    [783, 818],
    [771, 1077],
    [942, 1094], 
    [948, 826],
    [963, 521],
    [1124, 521],
    [1109, 816],
    [1082, 1119]
], dtype="float32")

# New robot points since someone kicked the camera
bunsen_robot_points_1 = np.array([
    [175, -841],
    [477, -838],
    [738, -849],
    [749, -615], 
    [474, -623],
    [177, -606],
    [170, -406],
    [448, -402],
    [769, -433]
], dtype="float32")

# functions to calculate homography matrix
def calculateBunsenHomography():
    homography_matrix, _ = cv2.findHomography(bunsen_image_points_1, bunsen_robot_points_1) 
    return (homography_matrix)


def calculateBeakerHomography():
    homography_matrix, _ = cv2.findHomography(beaker_image_points_2, beaker_robot_points_2) 
    return (homography_matrix)

print(calculateBeakerHomography())