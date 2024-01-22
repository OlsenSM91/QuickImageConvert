# I had to change from tkinter to PyQt and not use Pillow with the macOS version. This is the fix and the source for the macOS DMG/.app folder
import os
import argparse
import shutil
from PIL import Image
from io import BytesIO
from resizeimage import resizeimage
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt

MAX_SIZE = 15 * 1024 * 1024  # Default 15MB

class QuickImageConvertApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Quick Image Convert v0.3 G&H Designs")
        self.setGeometry(100, 100, 450, 250)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        input_label = QLabel("Input Directory:", central_widget)
        input_label.move(20, 20)

        self.input_entry = QLineEdit(central_widget)
        self.input_entry.setGeometry(150, 20, 200, 20)

        input_button = QPushButton("Browse", central_widget)
        input_button.setGeometry(360, 20, 80, 20)
        input_button.clicked.connect(self.update_input_directory)

        output_label = QLabel("Output Directory:", central_widget)
        output_label.move(20, 60)

        self.output_entry = QLineEdit(central_widget)
        self.output_entry.setGeometry(150, 60, 200, 20)

        output_button = QPushButton("Browse", central_widget)
        output_button.setGeometry(360, 60, 80, 20)
        output_button.clicked.connect(self.update_output_directory)

        format_label = QLabel("Output Format:", central_widget)
        format_label.move(20, 100)

        self.format_combo = QComboBox(central_widget)
        self.format_combo.addItems(["PNG", "JPEG", "GIF", "TIFF", "ICO"])
        self.format_combo.setGeometry(150, 100, 200, 20)

        size_label = QLabel("Max Size (MB):", central_widget)
        size_label.move(20, 140)

        self.size_entry = QLineEdit(central_widget)
        self.size_entry.setGeometry(150, 140, 200, 20)
        self.size_entry.setText("15")

        recursive_check = QCheckBox("Recursive", central_widget)
        recursive_check.move(20, 180)

        convert_button = QPushButton("Convert", central_widget)
        convert_button.setGeometry(150, 210, 100, 30)
        convert_button.clicked.connect(self.on_submit)

    def update_input_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if dir_path:
            self.input_entry.setText(dir_path)

    def update_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_entry.setText(dir_path)

    def on_submit(self):
        input_dir = self.input_entry.text()
        output_dir = self.output_entry.text()

        if not input_dir or not output_dir:
            QMessageBox.critical(self, "Error", "Please specify both input and output directories.")
            return

        format_choice = self.format_combo.currentText()
        max_size = int(float(self.size_entry.text()) * 1024 * 1024)
        recursive = self.sender().isChecked()

        convert_images(input_dir, output_dir, format=format_choice, max_size=max_size, recursive=recursive)
        QMessageBox.information(self, "Info", "Conversion complete!")

def find_optimal_quality(img, max_size):
    low, high = 1, 100
    while low <= high:
        mid = (low + high) // 2
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=mid)
        size = buffer.getbuffer().nbytes
        
        if size > max_size:
            high = mid - 1  # if over max_size, decrease quality
        elif size < max_size - 1024:  # allow 1KB tolerance below max_size
            low = mid + 1  # if well under max_size, increase quality
        else:
            return mid  # if within tolerance, return quality
        
    return high  # Return the highest quality under the max_size if exact size can't be achieved

def reduce_image_quality(img, max_size, format="JPEG"):
    if format.upper() == "JPEG":
        optimal_quality = find_optimal_quality(img, max_size)
        if optimal_quality != -1:
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=optimal_quality)
            return Image.open(buffer)
        return None  # or handle as per your requirement
    else:
        low, high = 0.5, 1.0
        buffer = BytesIO()  # Initialize a new buffer for non-JPEG images
        while high - low > 0.001:  # set a threshold for the desired precision
            scale_factor = (low + high) / 2
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            
            reduced_img = resizeimage.resize_thumbnail(img, new_size)
            reduced_img.save(buffer, format=format)
            size = buffer.tell()
            
            if size <= max_size:
                low = scale_factor
            else:
                high = scale_factor
        
        # Use the scale factor from the last iteration to create the final reduced image
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        reduced_img = resizeimage.resize_thumbnail(img, new_size)
        reduced_img.save(buffer, format=format)
        return Image.open(buffer)

def convert_images(input_dir, output_dir, format="PNG", max_size=MAX_SIZE, allowed_extensions=None, recursive=False):
    if not allowed_extensions:
        allowed_extensions = ['.png', '.jpeg', '.jpg', '.gif', '.tiff', '.ico']

    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(tuple(allowed_extensions)):
                img = Image.open(file_path)
                new_name = os.path.splitext(os.path.basename(file_path))[0] + f".{format.lower()}"
                new_path = os.path.join(output_dir, new_name)

                if os.path.getsize(file_path) > max_size:
                    img = reduce_image_quality(img, max_size, format=format)
                    if img:
                        img.save(new_path, format=format)
                else:
                    shutil.copy(file_path, new_path)

                exported_size = os.path.getsize(new_path) / (1024 * 1024)  # Convert size from bytes to megabytes
                print(f"{new_name} exported with size: {exported_size:.2f} MB")

        if not recursive:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert image files with a size limit.")
    parser.add_argument("-i", "--input", default=os.getcwd(), help="Input directory containing image files. Defaults to current directory.")
    parser.add_argument("-o", "--output", required=True, help="Output directory to save the converted images.")
    parser.add_argument("--format", default="PNG", choices=["PNG", "JPEG", "GIF", "TIFF", "ICO"], help="Output format for the converted images.")
    parser.add_argument("--max_size", type=int, default=15, help="Maximum file size in MB.")
    allowed_extensions = ['.png', '.jpeg', '.jpg', '.gif', '.tiff', '.ico']

    app = QApplication(sys.argv)
    window = QuickImageConvertApp()
    window.show()
    sys.exit(app.exec_())
