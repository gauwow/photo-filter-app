# Photo Filter App

A simple Python application that allows you to load images, apply various filters, rotate images, and save the processed results. The app displays the original image and the processed image side by side for easy comparison, with performance optimizations and enhanced UI features.

## Features
- Load images in common formats (PNG, JPG, JPEG, BMP, GIF).
- Apply a wide range of filters:
  - Black and White (Grayscale)
  - Vivid Cool (Enhance cool tones like blues and greens)
  - Retro (Vintage, muted effect)
  - Sepia (Warm, brownish vintage tone)
  - Warm Glow (Enhance reds and yellows for a cozy effect)
  - Sharpen (Enhance edges and details)
  - High Contrast (Increase contrast for a dramatic look)
  - Pencil Sketch (Convert to a grayscale sketch with dark lines)
  - Blur (Softens the image with a Gaussian blur)
  - Vintage Polaroid (Mimic old Polaroid photos with faded colors and a yellowed border)
- Rotate both original and processed images 90° clockwise.
- Save processed images in PNG or JPEG format.
- Dynamic resizing to maintain aspect ratios, with optimized processing for performance (resizes to 800x600 max for processing, 400x400 max for display).
- Labels under each image: "Original" (left) and "Processed" (right), with dynamic bolding when filters, rotations, or saves are applied.
- Processing time counter showing how long each filter or rotation takes.
- Square buttons arranged horizontally, with highlighting (sunken border) when selected.
- Filters reset to the original image before applying a new filter, ensuring each filter starts fresh.

## Prerequisites
- Python 3.8 or higher
- Required libraries:
  - `Pillow` (for image processing)
  - `tkinter` (for the GUI, usually included with Python)
  - `numpy` (for performance-optimized pixel-by-pixel filters, install with `pip install numpy`)

## Installation
1. Clone this repository or download the `photo_filter_app.py` file:
   ```bash
   git clone https://github.com/gauwow/photo-filter-app.git
   cd photo-filter-app
