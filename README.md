# Leaf Area Analyzer for Citrus 

A **Python-based tool** for measuring leaf area from scanned images using OpenCV and multi-color masking techniques.



##  Features:
- Calculates **total, average, and individual leaf areas** (cm²)
- Detects **different color variations and shapes** of leaves
- Exports results to **CSV files** and saves **processed images** with contours and leaf numbering



## 🚀 How to Use:

1. **Prepare Your Images:**
   - Place your **scanned leaf images** and a **reference image with the scale** (named `scale_image.jpg`) in the same folder.

2. **Set Up the Script:**
   - Copy or download the script into your Python environment.
   - Install the required libraries:
     ```bash
     pip install opencv-python numpy pandas
     ```

3. **Check Input and Output Paths:**
   - Open the `.py` file and make sure the **input** and **output** folder paths match your folder structure containing the images and the location for where the files will be saved.

4. **Watch the Tutorial:**
   - 📹 [Click here to watch the video instructions](https://youtu.be/bThS7Iwn94A)

5. **Run the Script:**
   - Follow the on-screen instructions to **set the scale** by clicking two points exactly 1 cm apart on the ruler image.
   - The script will automatically process the images.



## 📄 Outputs:
- A folder named `Processed` containing images with contours and leaf numbers.
- Two Excel files:
  1. **Individual Leaf Areas:** Leaf area for each leaf in every image.
  2. **Leaf_Area_Results:** Total number of leaves and average leaf area per image.



## 💡 Tips for Success:
- Make sure images are **scanned clearly and uniformly**, with no touching between leaves and each leaf scanned fully on the scanner bed.
- Don’t forget the **scale image** for accurate area calculations.
- Verify the **input/output** folder paths before running.



## 🙋 Need Help?
Contact: **Emilio Suarez**  
📧 eps98075@uga.edu

Feel free to modify this code and try it on **other leaf types, crops, or research applications**—and remember to **cite us** if you use this tool in your work!
