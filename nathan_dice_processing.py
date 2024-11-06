import cv2
import numpy as np
import json

def count_black_pips(dice_face):
    if dice_face is None or dice_face.size == 0:
        print("Error with dice face")
        return 0
    gray = cv2.cvtColor(dice_face, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)
    pip_contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pip_count = 0
    for contour in pip_contours:
        area = cv2.contourArea(contour)
        if area > 500 and area < 2500:
            pip_count += 1
            # cv2.drawContours(dice_face, [contour], -1, (255, 0, 0), 2)  # Draw in blue color
            # cv2.imshow('dice', dice_face)
            # cv2.waitKey(0)

    return pip_count

def main():
    image = cv2.imread('dice.png')
    if image is None:
        print("Error: Could not read the image.")
        return 0
    filtered_image = cv2.bilateralFilter(image, d=10, sigmaColor=50, sigmaSpace=20)
    hsv = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([28, 100, 130])
    upper_yellow = np.array([35, 255, 200])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dice_info = []

    for contour in contours:
        area = cv2.contourArea(contour)
        rect = cv2.minAreaRect(contour)
        if area < 28000 or area > 50000:
            continue
        if rect[1][0] < 170 or rect[1][0] > 230:
            continue

        center_x, center_y = int(rect[0][0]), int(rect[0][1])
        angle = round(rect[2],2)
        
        box = cv2.boxPoints(rect).astype(int)
        # cv2.drawContours(image, [box], 0, (0, 255, 0), 8)
        cv2.drawContours(image, [contour], 0, (0, 255, 0), 8)

        width, height = int(rect[1][0] * 0.8), int(rect[1][1] * 0.8)
        dice = image[center_y - height//2 : center_y + height//2, center_x - width//2 : center_x + width//2]

        pip_count = count_black_pips(dice)

        cv2.putText(image, f'Pips:{int(rect[0][0])}', (int(rect[0][0]-100), int(rect[0][1])+200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 8)
        # Store the location, rotation, and pip count of the dice as a JSON object
        dice_info.append({
            'x': center_x,
            'y': center_y,
            'rot': angle,
            'pips': pip_count,
        })

    # Convert the dice information to JSON file
    dice_info_json = json.dumps(dice_info, indent=4)
    with open('dice_info.json', 'w') as json_file:
        json_file.write(dice_info_json)

    final = cv2.resize(image, (0, 0), fx=0.2, fy=0.2)
    cv2.imshow('Detected Dice', final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


