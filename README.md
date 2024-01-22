# Quick Image Convert v0.3

Quick Image Convert v0.3 is a handy tool designed to convert image files while allowing users to define the output directory, format, maximum file size, and whether the operation should be carried out recursively through subdirectories.

![Screenshot 2023-10-04 001555](https://github.com/OlsenSM91/QuickImageConvert/assets/130707762/619d9e3c-a40b-468c-b210-712dbefe18e1)


## Features

- Convert images to different formats (PNG, JPEG, GIF, TIFF, ICO)
- Specify a maximum file size for images.
- Optional recursive operation through subdirectories.
- Graphical User Interface for easy operation.
- Console operation also supported with arguments.
- Updated to include a macOS version and compiled binary/dmg

## Dependencies

- Python 3
- PIL (Pillow) (Windows)
- python-image-resize (macOS)
- Tkinter (Winters)
- PyQt5 (macOS)

## Usage

### GUI Mode:

1. Run `QuickImageConvertv0.3.py` without any arguments to launch the GUI.
2. Fill in the "Input Directory" and "Output Directory" fields, or use the "Browse" buttons to select directories.
3. Choose the desired "Output Format" from the drop-down menu.
4. Specify the "Max Size (MB)" to set a maximum file size for the output images.
5. Check the "Recursive" checkbox if you wish to process images in subdirectories recursively.
6. Click the "Convert" button to start the conversion process.

### Console Mode:

Run the script with arguments to operate in console mode:

```bash
python QuickImageConvertv0.3.py -i [input_directory] -o [output_directory] --format [format] --max_size [max_size_in_MB]
```

Example:

```bash
python QuickImageConvertv0.3.py -i /path/to/input -o /path/to/output --format PNG --max_size 15
```

## Building Executable

To build an executable for Windows or macOS, you can use a packaging tool like `PyInstaller` or `auto-py-to-exe`. 

Example using PyInstaller:

```bash
pyinstaller --onefile --windowed QuickImageConvertv0.3.py
```

For more advanced packaging options, including setting an icon or hiding the console window, `auto-py-to-exe` provides a graphical interface for packaging Python scripts into executables.

## Troubleshooting

In case your antivirus software flags the generated executable as a potential threat, this is likely a false positive. Please refer to the script documentation for steps on how to resolve this issue.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/OlsenSM91/QuickImageConvertv0.3/issues).
