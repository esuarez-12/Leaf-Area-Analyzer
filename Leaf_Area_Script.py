"""
Leaf Area Analyzer
Version: Ver04_MultiColor_Leaves
Author: Emilio Suarez

"""

import cv2
import numpy as np
import os
import pandas as pd

# USER SETTINGS
folder_path = os.path.join(os.getcwd(), 'input')
scale_image_path = os.path.join(folder_path, 'scale_image.jpg')
output_folder = os.path.join(os.getcwd(), 'output')
output_csv = os.path.join(output_folder, 'Leaf_Area_Results.csv')
output_csv_individual = os.path.join(output_folder, 'Individual_Leaf_Areas.csv')

os.makedirs(output_folder, exist_ok=True)

# FUNCTION: SCALE SETUP
def set_scale(image_path):
    img = cv2.imread(image_path)
    points = []

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(img_copy, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Set Scale - Click two points 1 cm apart', img_copy)

    img_copy = img.copy()
    cv2.imshow('Set Scale - Click two points 1 cm apart', img_copy)
    cv2.setMouseCallback('Set Scale - Click two points 1 cm apart', click_event)

    print("👉 Click two points on the scale image that are exactly 1 cm apart.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(points) != 2:
        raise ValueError("Error: You must click exactly two points.")

    dist_pixels = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
    pixels_per_cm = dist_pixels / 1.0
    print(f"✅ Scale set: {pixels_per_cm:.2f} pixels = 1 cm")
    return pixels_per_cm

# FUNCTION: LEAF IMAGE PROCESSING 
def process_leaf_image(image_path, pixels_per_cm, output_folder):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([25, 40, 40])
    upper_green = np.array([90, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    lower_brown = np.array([10, 40, 20])
    upper_brown = np.array([30, 255, 200])
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)

    lower_yellow = np.array([15, 80, 120])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    mask_combined = cv2.bitwise_or(mask_green, mask_brown)
    mask_combined = cv2.bitwise_or(mask_combined, mask_yellow)

    kernel = np.ones((5, 5), np.uint8)
    cleaned = cv2.morphologyEx(mask_combined, cv2.MORPH_OPEN, kernel, iterations=2)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, hierarchy = cv2.findContours(cleaned, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_with_contours = img.copy()
    leaf_areas_cm2 = []

    min_leaf_area_cm2 = 0.5
    min_leaf_area_pixels = min_leaf_area_cm2 * (pixels_per_cm ** 2)

    for i, contour in enumerate(contours):
        area_pixels = cv2.contourArea(contour)
        if area_pixels > min_leaf_area_pixels and (hierarchy[0][i][3] == -1):
            epsilon = 0.0025 * cv2.arcLength(contour, True)
            contour_smooth = cv2.approxPolyDP(contour, epsilon, True)

            area_cm2 = area_pixels / (pixels_per_cm ** 2)
            leaf_areas_cm2.append(area_cm2)

            cv2.drawContours(img_with_contours, [contour_smooth], -1, (0, 0, 255), 2)
            M = cv2.moments(contour_smooth)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.putText(img_with_contours, str(len(leaf_areas_cm2)), (cX, cY),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

    total_leaf_area = sum(leaf_areas_cm2)
    num_leaves = len(leaf_areas_cm2)
    avg_leaf_area = total_leaf_area / num_leaves if num_leaves else 0

    output_image_name = os.path.basename(image_path).replace('.jpg', '_contours.jpg')
    output_image_path = os.path.join(output_folder, output_image_name)
    cv2.imwrite(output_image_path, img_with_contours)

    return total_leaf_area, num_leaves, avg_leaf_area, leaf_areas_cm2

# MAIN SCRIPT 
if __name__ == '__main__':
    results = []
    individual_leaf_data = []

    pixels_per_cm = set_scale(scale_image_path)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff')) and filename != os.path.basename(scale_image_path):
            image_path = os.path.join(folder_path, filename)
            print(f"📷 Processing {filename}...")

            total_area, num_leaves, avg_area, leaf_areas = process_leaf_image(image_path, pixels_per_cm, output_folder)

            results.append({
                'Image Name': filename,
                'Total Leaf Area (cm²)': round(total_area, 2),
                'Number of Leaves': num_leaves,
                'Average Leaf Area (cm²)': round(avg_area, 2)
            })

            for i, leaf_area in enumerate(leaf_areas, start=1):
                individual_leaf_data.append({
                    'Image Name': filename,
                    'Leaf #': i,
                    'Leaf Area (cm²)': round(leaf_area, 2)
                })

    df_summary = pd.DataFrame(results)
    df_summary.to_csv(output_csv, index=False)

    df_individual = pd.DataFrame(individual_leaf_data)
    df_individual.to_csv(output_csv_individual, index=False)

    print(f"\n✅ All done! Results saved to:\n{output_csv}")
    print(f"📄 Individual leaf areas saved to:\n{output_csv_individual}")
    print(f"🖼 Processed images saved to:\n{output_folder}")

