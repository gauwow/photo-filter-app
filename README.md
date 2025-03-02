# Photo Filter App

A simple Python application that allows you to load images, apply various filters (e.g., black and white, vivid cool, retro), rotate images, and save the processed results. The app displays the original image and the processed image side by side for easy comparison.

## Features
- Load images in common formats (PNG, JPG, JPEG, BMP, GIF).
- Apply filters:
  - Black and White (Grayscale)
  - Vivid Cool (Enhance cool tones like blues and greens)
  - Retro (Vintage, muted effect)
- Rotate images 90° clockwise (applies to both original and processed images).
- Save processed images in PNG or JPEG format.
- Dynamic resizing to maintain aspect ratios for display.

## Prerequisites
- Python 3.8 or higher
- Required libraries:
  - `Pillow` (for image processing)
  - `tkinter` (for the GUI, usually included with Python)

## Installation
1. Clone this repository or download the `photo_filter_app.py` file:
   ```bash
   git clone <https://github.com/gauwow/photo-filter-app>
   cd photo-filter-app
