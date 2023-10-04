import os
import argparse
import shutil
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys

MAX_SIZE = 15 * 1024 * 1024  # Default 15MB

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
        # For non-JPG, use binary search to find the optimal scale factor
        low, high = 0.5, 1.0
        buffer = BytesIO()  # Initialize a new buffer for non-JPEG images
        while high - low > 0.001:  # set a threshold for the desired precision
            scale_factor = (low + high) / 2
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            reduced_img = img.resize(new_size, Image.ANTIALIAS)
            buffer.seek(0)
            buffer.truncate()
            reduced_img.save(buffer, format=format)
            size = buffer.getbuffer().nbytes
            if size <= max_size:
                low = scale_factor
            else:
                high = scale_factor
        
        # Use the scale factor from the last iteration to create the final reduced image
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        reduced_img = img.resize(new_size, Image.ANTIALIAS)
        buffer.seek(0)
        buffer.truncate()
        reduced_img.save(buffer, format=format)
        
        return Image.open(buffer)

def get_image_format(img):
    return img.format if img.format else "JPEG"  # Default to JPEG if format is None

def convert_images(input_dir, output_dir, format="PNG", max_size=MAX_SIZE, allowed_extensions=None, recursive=False):
    if not allowed_extensions:
        allowed_extensions = ['.png', '.jpeg', '.jpg', '.gif', '.tiff', '.ico']
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(tuple(allowed_extensions)):
                img = Image.open(file_path)
                new_name = os.path.splitext(os.path.basename(file_path))[0] + f".{format.lower()}"
                
                # Debugging lines
                print(f'Output Directory: {output_dir}')  
                print(f'New Name: {new_name}')  
                
                new_path = os.path.join(output_dir, new_name)
                
                # Debugging line
                print(f'New Path: {new_path}')  
                
                if os.path.getsize(file_path) > max_size:
                    img = reduce_image_quality(img, max_size, format=format)
                    img.save(new_path, format)
                else:
                    # Copy the image to the output directory if it's under the limit
                    shutil.copy(file_path, new_path)
                
                # Print the name and size of the exported file
                exported_size = os.path.getsize(new_path) / (1024 * 1024)  # Convert size from bytes to megabytes
                print(f"{new_name} exported with size: {exported_size:.2f} MB")
        
        # Break out of os.walk early if recursive is False
        if not recursive:
            break

# GUI Functions
def on_submit():
    input_dir = input_entry.get()
    output_dir = output_entry.get()

    # Debugging line
    print(f'Output Directory in on_submit: {output_dir}')

    # Additional Debugging lines
    print(f'Output Entry Content in on_submit: {output_entry.get()}')

    if not input_dir or not output_dir:
        messagebox.showerror("Error", "Please specify both input and output directories.")
        return

    # Reset the output_entry widget to ensure it contains the correct value
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

    # Additional Debugging lines
    print(f'Output Directory after reset: {output_entry.get()}')

    format_choice = format_var.get()
    max_size = int(float(size_var.get()) * 1024 * 1024)
    recursive = bool(recursive_var.get())  # Convert to boolean
    convert_images(input_dir, output_dir, format=format_choice, max_size=max_size, recursive=recursive)
    messagebox.showinfo("Info", "Conversion complete!")

def update_input_directory():
    dir_path = filedialog.askdirectory()
    if dir_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, dir_path)

def update_output_directory():
    dir_path = filedialog.askdirectory()
    if dir_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, dir_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert image files with a size limit.")
    parser.add_argument("-i", "--input", default=os.getcwd(), help="Input directory containing image files. Defaults to current directory.")
    parser.add_argument("-o", "--output", required=True, help="Output directory to save the converted images.")
    parser.add_argument("--format", default="PNG", choices=["PNG", "JPEG", "GIF", "TIFF", "ICO"], help="Output format for the converted images.")
    parser.add_argument("--max_size", type=int, default=15, help="Maximum file size in MB.")
    allowed_extensions = ['.png', '.jpeg', '.jpg', '.gif', '.tiff', '.ico']

    if len(sys.argv) == 1:
        # No arguments, launch GUI
        # Create the GUI
        root = tk.Tk()
        root.title("Quick Image Convert v0.3 G&H Designs")

        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input Directory
        ttk.Label(frame, text="Input Directory:").grid(column=0, row=0, sticky=tk.W, pady=5)
        input_entry = ttk.Entry(frame, width=40)
        input_entry.grid(column=1, row=0, pady=5)
        ttk.Button(frame, text="Browse", command=update_input_directory).grid(column=2, row=0, pady=5)

        # Output Directory
        ttk.Label(frame, text="Output Directory:").grid(column=0, row=1, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(frame, width=40)
        output_entry.grid(column=1, row=1, pady=5)
        ttk.Button(frame, text="Browse", command=update_output_directory).grid(column=2, row=1, pady=5)  # updated here

        # Output Format
        ttk.Label(frame, text="Output Format:").grid(column=0, row=2, sticky=tk.W, pady=5)
        format_var = tk.StringVar(value="PNG")
        ttk.Combobox(frame, textvariable=format_var, values=["PNG", "JPEG", "GIF", "TIFF", "ICO"]).grid(column=1, row=2, pady=5, sticky=tk.W)

        # Max File Size
        ttk.Label(frame, text="Max Size (MB):").grid(column=0, row=3, sticky=tk.W, pady=5)
        size_var = tk.StringVar(value="15")
        ttk.Entry(frame, textvariable=size_var, width=10).grid(column=1, row=3, pady=5, sticky=tk.W)

        # Recursive Checkbox
        recursive_var = tk.IntVar(value=1)  # Default to recursive
        recursive_check = tk.Checkbutton(frame, text="Recursive", variable=recursive_var)
        recursive_check.grid(column=1, row=4, pady=5, sticky=tk.W)

        # Submit button
        ttk.Button(frame, text="Convert", command=on_submit).grid(column=1, row=5, pady=20)

        root.mainloop()
    else:
        args = parser.parse_args()
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        convert_images(args.input, args.output, format=args.format, max_size=args.max_size * 1024 * 1024, allowed_extensions=allowed_extensions)
