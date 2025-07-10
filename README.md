Leaf Area Analyzer for Citrus 🍃
A Python-based tool for measuring leaf area from scanned images using OpenCV and multi-color masking techniques.

✨ Features:
Calculates total, average, and individual leaf areas (cm²)

Detects different color variations and shapes of leaves

Exports results to CSV files and saves processed images with contours and leaf numbering

🚀 How to Use:
Prepare Your Images:

Place your scanned leaf images and a scanned ruler image (named scale_image.jpg) in the same folder.

Set Up the Script:

Copy or download the script into your Python environment.

Install the required libraries:

bash
Copy
Edit
pip install opencv-python numpy pandas
Check Input and Output Paths:

Open the .py file and make sure the input and output folder paths match your folder structure.

Watch the Tutorial:

📺 Click here to watch the video instructions

Run the Script:

Follow the on-screen instructions to set the scale by clicking two points exactly 1 cm apart on the ruler image.

The script will automatically process the images.

📄 Outputs:
A folder named Processed containing images with contours and leaf numbers.

Two Excel files:

Individual Leaf Areas: Leaf area for each leaf in every image.

Summary Results: Total number of leaves and average leaf area per image.

💡 Tips for Success:
Make sure images are scanned clearly and uniformly.

Don’t forget the scale image for accurate area calculations.

Verify the input/output folder paths before running.

🙋 Need Help?
Contact: Emilio Suarez
📧 eps98075@uga.edu

Feel free to modify this code and try it on other leaf types, crops, or research applications!

📜 License:
Licensed under the MIT License.

