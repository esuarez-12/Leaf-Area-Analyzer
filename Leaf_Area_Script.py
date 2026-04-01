# Leaf Area Analyzer v1.1
#Author: Emilio Suarez
#Date: April 2026
# ------------------------------------------------
# 🚨 USER INSTRUCTIONS:
# 1. Replace the paths below with your own local folders/files.
# 2. Ensure your folder contains the leaf images AND the scale image (1 cm reference).
# ------------------------------------------------

"""
Citrus Leaf Area Analyzer (Ver 1.1)
"""

import cv2
import numpy as np
import os
import pandas as pd

# === SETTINGS (USER must edit these paths) ===
base_folder = r'YOUR_FOLDER_PATH_HERE'           # <-- e.g. r'C:\Users\YourName\Desktop\Leaves'
scale_image_name = 'scale_image.jpg'             # <-- Name of your ruler image (must be inside base_folder)
scale_image_path = os.path.join(base_folder, scale_image_name)

output_csv = os.path.join(base_folder, 'Leaf_Area_Results.csv')
output_csv_individual = os.path.join(base_folder, 'Individual_Leaf_Areas.csv')
output_image_folder = os.path.join(base_folder, 'Processed')
os.makedirs(output_image_folder, exist_ok=True)

def set_scale(image_path):
    """
    Initializes pixel-to-cm calibration via manual input.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Scale image not found: {image_path}")
    
    points = []
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(img_copy, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Calibration', img_copy)

    img_copy = img.copy()
    cv2.imshow('Calibration', img_copy)
    cv2.setMouseCallback('Calibration', click_event)

    print("Action Required: Click two points 1 cm apart on the scale image.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(points) != 2:
        raise ValueError("Calibration failed: Two points required.")

    dist_pixels = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
    return dist_pixels

def process_leaf_image(image_path, pixels_per_cm, output_folder):
    """
    Performs color segmentation and morphological separation on leaf samples.
    """
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask_green = cv2.inRange(hsv, np.array([20, 20, 20]), np.array([100, 255, 255]))
    mask_dark = cv2.inRange(hsv, np.array([10, 5, 5]), np.array([110, 255, 120]))
    mask_combined = cv2.bitwise_or(mask_green, mask_dark)

    kernel_3 = np.ones((3, 3), np.uint8)
    kernel_5 = np.ones((5, 5), np.uint8)
    
    closed = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel_5, iterations=2)
    
    cnts_fill, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled_mask = np.zeros_like(closed)
    for c in cnts_fill:
        cv2.drawContours(filled_mask, [c], -1, 255, -1)

    eroded = cv2.erode(filled_mask, kernel_3, iterations=6)
    num_labels, labels = cv2.connectedComponents(eroded)
    
    final_contours = []
    min_area_px = 0.5 * (pixels_per_cm ** 2)

    for i in range(1, num_labels):
        leaf_seed = np.uint8(labels == i) * 255
        recovered = cv2.dilate(leaf_seed, kernel_3, iterations=12)
        recovered = cv2.bitwise_and(recovered, filled_mask)
        
        cnts, _ = cv2.findContours(recovered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if cnts:
            c = max(cnts, key=cv2.contourArea)
            if cv2.contourArea(c) > min_area_px:
                epsilon = 0.0002 * cv2.arcLength(c, True)
                final_contours.append(cv2.approxPolyDP(c, epsilon, True))

    img_out = img.copy()
    leaf_areas = []

    for i, contour in enumerate(final_contours, 1):
        area_cm2 = cv2.contourArea(contour) / (pixels_per_cm ** 2)
        leaf_areas.append(area_cm2)

        cv2.drawContours(img_out, [contour], -1, (0, 0, 255), 2)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            cv2.putText(img_out, str(i), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    cv2.imwrite(os.path.join(output_folder, f"{base_name}_Processed.jpg"), img_out)

    return sum(leaf_areas), len(leaf_areas), (sum(leaf_areas)/len(leaf_areas) if leaf_areas else 0), leaf_areas

if __name__ == '__main__':
    summary_results = []
    individual_results = []

    try:
        px_cm = set_scale(scale_image_path)
        valid_exts = ('.jpg', '.jpeg', '.png', '.tif', '.tiff')
        files = [f for f in os.listdir(base_folder) if f.lower().endswith(valid_exts) and f != scale_image_name]

        for filename in files:
            print(f"Processing: {filename}")
            total_area, count, avg_area, leaf_list = process_leaf_image(
                os.path.join(base_folder, filename), px_cm, output_image_folder
            )

            summary_results.append({
                'Image Name': filename,
                'Total Leaf Area (cm²)': round(total_area, 2),
                'Number of Leaves': count,
                'Average Leaf Area (cm²)': round(avg_area, 2)
            })

            for i, area in enumerate(leaf_list, 1):
                individual_results.append({
                    'Image Name': filename,
                    'Leaf #': i,
                    'Leaf Area (cm²)': round(area, 3)
                })

        pd.DataFrame(summary_results).to_csv(output_csv, index=False)
        pd.DataFrame(individual_results).to_csv(output_csv_individual, index=False)

        print(f"\n✅ Analysis complete. Results saved to CSV in: {base_folder}")

    except Exception as e:
        print(f"❌ Error: {e}")

