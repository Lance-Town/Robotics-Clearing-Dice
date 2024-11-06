from homography import calculateBunsenHomography, calculateBeakerHomography
import image_capture_demo
import cv2
import json
import numpy as np

# Function to transform points using homography with numpy wizardry
def transform_points(points, homography):
    # Convert points to homogeneous coordinates
    points_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))  # Add a column of 1s for homogeneous coordinates
    transformed_points = homography @ points_homogeneous.T  # Apply homography
    transformed_points /= transformed_points[-1, :]  # Normalize by the last row
    return transformed_points[:2, :].T  # Return only x and y coordinates


# Capture image, saved to './dice.png'
def getImage():
    res = image_capture_demo.main()

    if (res != 0):
        exit(1)

def detectDice(showImg = True):
    # capture the image
    getImage()

    # Load the image
    image = cv2.imread('./dice.png')

    # image = cv2.resize(image, (0, 0), fx=0.2, fy=0.2)
    image = cv2.resize(image, (1200, 1200))

    # Convert to HSV to isolate yellow color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range for yellow color in HSV
    lower_yellow = np.array([28, 100, 150])
    upper_yellow = np.array([50, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Apply mask to get only yellow regions
    yellow_regions = cv2.bitwise_and(image, image, mask=mask)

    # Convert to grayscale for further processing
    gray = cv2.cvtColor(yellow_regions, cv2.COLOR_BGR2GRAY)
    
    # Apply mask to get just black and white image
    _, mask = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY)

    # Find contours to detect dice
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the homography
    bunsen_homography_matrix = calculateBunsenHomography()
    beaker_homography_matrix = calculateBeakerHomography()

    BeakerCoordinates = []
    BunsenCoordinates = []

    for contour in contours:
        isBunsen = True # Flag to default to bunsen

        # Filter out the small and large areas to only get the dice
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        # print(f"{area} ------ {perimeter}")
        if (area < 1000  or area > 20000):
            continue
    
        # Find minimum area rectangle for each contour to get orientation
        rect = cv2.minAreaRect(contour)
        # box = cv2.boxPoints(rect)
        box = cv2.boxPoints(rect).astype(int)
        box = np.int32(box)

        # Transform the corners of the bounding box using the homography matrix
        transformed_box = transform_points(box, bunsen_homography_matrix)

        # if (transformed_box[0][1] < -1550):
        if (rect[0][0] < 415):
            # This will be beakers dice to grab
            print("This is beakers")
            transformed_box = transform_points(box, beaker_homography_matrix)
            isBunsen = False

        if (perimeter > 750):
            # we probably have multiple dice in one area. Need to split this up better
            print("This is a region with two dice in it, need to do something about this")

        # Draw the bounding box on the original image
        cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
        # cv2.drawContours(image, [contour], 0, (0, 255, 0), 2)
    
        # Calculate center and angle
        center = (int(rect[0][0]), int(rect[0][1]))
        angle = rect[2]

        # Get the angle in a nice degree the robot can use
        if angle < -45:
                angle = 90 + angle

        angle = 90 - angle 


        # Beaker needs to have about a 30 degree translation
        if (not isBunsen):
            angle += 27 

        # Draw center and angle
        cv2.circle(image, center, 5, (255, 0, 0), -1)
        cv2.putText(image, f"Angle: {int(angle)}", (center[0] + 20, center[1]), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # Draw the transformed box
        transformed_box = np.int32(transformed_box)  
        # cv2.drawContours(image, [transformed_box], 0, (0, 255, 0), 2)

        # Get the center point of the dice
        transformed_center = np.mean(transformed_box, axis=0).astype(int)

        # If the detected "dice" is -160 or less in x direction, then it isn't a dice as this is off table
        if (transformed_center[0] < -160):
            continue

        # Format the robot coordinates as a string
        coordinates_text = f"({transformed_center[0]}, {transformed_center[1]})"

        if isBunsen:
            # Add the coordinates to beakers coordinates for the return value
            BunsenCoordinates.append({"pos": [int(transformed_center[0]), int(transformed_center[1]), -170, -177, -4, int(angle)]})
        else:
            BeakerCoordinates.append({"pos": [int(transformed_center[0]), int(transformed_center[1]), -126, 178, -2, int(angle)]})

        # Draw the transformed coordinates above the dice
        cv2.putText(image, coordinates_text, (center[0], center[1]-50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite("detectedDice.png", image)
    if (showImg):
        # Show the results
        cv2.imshow("Detected Dice", mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return [json.dumps(BunsenCoordinates), json.dumps(BeakerCoordinates)]


if __name__ == '__main__':
    print(detectDice())