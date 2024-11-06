# from homography import calculateBunsenHomography, calculateBeakerHomography
# import image_capture_demo
# import cv2
# import json
# import numpy as np

# # Function to transform points using homography with numpy wizardry
# def transform_points(points, homography):
#     # Convert points to homogeneous coordinates
#     points_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))  # Add a column of 1s for homogeneous coordinates
#     transformed_points = homography @ points_homogeneous.T  # Apply homography
#     transformed_points /= transformed_points[-1, :]  # Normalize by the last row
#     return transformed_points[:2, :].T  # Return only x and y coordinates


# # Capture image, saved to './dice.png'
# def getImage():
#     res = image_capture_demo.main()

#     if (res != 0):
#         exit(1)

# def detectDice(showImg = True):
#     # capture the image
#     # getImage()

#     # Load the image
#     image = cv2.imread('./dice.png')
#     # image = cv2.resize(image, (0, 0), fx=0.2, fy=0.2)
#     image = cv2.resize(image, (1200, 1200))

#     # Convert to HSV to isolate yellow color
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Define range for yellow color in HSV
#     lower_yellow = np.array([28, 255, 150])
#     upper_yellow = np.array([50, 255, 255])
#     mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

#     # Apply mask to get only yellow regions
#     yellow_regions = cv2.bitwise_and(image, image, mask=mask)

#     # Convert to RGB for more processing 
#     rgb = cv2.cvtColor(yellow_regions, cv2.COLOR_BGR2RGB)

#     # Convert to grayscale for further processing
#     gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    
#     # Apply mask to get just black and white image
#     _, mask = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY)

#     # binary = cv2.bitwise_and(gray, gray, mask=mask)
#     # blurred = cv2.GaussianBlur(mask, (5, 5), 0)
#     # blurred = cv2.bilateralFilter(mask, 9, 75, 75)

#     # edges = cv2.Canny(blurred, 120, 150)

#     # Find contours to detect dice
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Get the homography
#     bunsen_homography_matrix = calculateBunsenHomography()
#     beaker_homography_matrix = calculateBeakerHomography()

#     # print("HOMOGRAPHY MATRIX: ", homography_matrix)

#     BeakerCoordinates = []

#     for contour in contours:
#         # Filter out the small and large areas to only get the dice
#         area = cv2.contourArea(contour)
#         perimeter = cv2.arcLength(contour, True)
#         # print(f"{area} ------ {perimeter}")
#         if (area < 3000 or area > 600000):
#             continue
    
#         # Find minimum area rectangle for each contour to get orientation
#         rect = cv2.minAreaRect(contour)
#         box = cv2.boxPoints(rect)
#         box = np.int32(box)
#         # ellipse = cv2.fitEllipse(contour)
#         # cv2.ellipse(image,ellipse,(0,255,0),2)
#         # (x,y),radius = cv2.minEnclosingCircle(contour)
#         # center = (int(x),int(y))
#         # radius = int(radius)
#         # cv2.circle(image,center,radius,(0,255,0),2)

#         print(f"rect: {rect}")

#         # Transform the corners of the bounding box using the homography matrix
#         transformed_box = transform_points(box, bunsen_homography_matrix)

#         # Check the detected point is on the table or not in Bunsens space
#         if (transformed_box[0][0] < 0):
#             continue

#         if (perimeter > 750):
#             # we probably have multiple dice in one area. Need to split this up better
#             print("This is a region with two dice in it, need to do something about this")

#         # Draw the bounding box on the original image
#         cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
    
#         # Calculate center and angle
#         center = (int(rect[0][0]), int(rect[0][1]))
#         angle = rect[2]

#         # Get the angle in a nice degree the robot can use
#         if angle < -45:
#             angle = 90 + angle

#         angle = 90 - angle 
    
#         # Draw center and angle
#         cv2.circle(image, center, 5, (255, 0, 0), -1)
#         cv2.putText(image, f"Angle: {int(angle)}", (center[0] + 20, center[1]), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)


#         # Draw the transformed box
#         transformed_box = np.int32(transformed_box)  
#         cv2.drawContours(image, [transformed_box], 0, (0, 0, 255), 2)

#         # Get the center point of the dice
#         transformed_center = np.mean(transformed_box, axis=0).astype(int)

#         # Format the robot coordinates as a string
#         coordinates_text = f"({transformed_center[0]}, {transformed_center[1]})"

#         # if transformed_box[0][1] > -1000:
#             # Add the coordinates to beakers coordinates for the return value
#         BeakerCoordinates.append({"pos": [int(transformed_center[0]), int(transformed_center[1]), -170, -177, -4, int(angle)]})

#         # Draw the transformed coordinates above the dice
#         cv2.putText(image, coordinates_text, (center[0], center[1]-50), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     cv2.imwrite("detectedDice.png", image)
#     if (showImg):
#         # Show the results
#         cv2.imshow("Detected Dice", image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

#     return json.dumps(BeakerCoordinates)

# if __name__ == '__main__':
#     print(detectDice())