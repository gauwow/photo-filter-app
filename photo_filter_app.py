import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw
import time
import numpy as np


class PhotoFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "Photo Filter App - Original and Processed Side by Side")
        # Wider window to accommodate buttons and images
        self.root.geometry("1200x600")

        # Track the last selected button for highlighting
        self.last_button = None

        # Create a frame to hold the original and processed images side by side
        self.content_frame = tk.Frame(root)
        self.content_frame.pack(pady=20, padx=10, fill="both", expand=True)

        # Left frame for the original image (unchanged)
        self.left_frame = tk.Frame(self.content_frame, width=400)
        self.left_frame.pack(side="left", padx=10, fill="both", expand=True)

        # Right frame for the main (processed) image
        self.right_frame = tk.Frame(self.content_frame, width=400)
        self.right_frame.pack(side="right", padx=10, fill="both", expand=True)

        # Create a frame for buttons (horizontal layout, square buttons)
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10, fill="x")

        # Square buttons (40x40 pixels) next to each other with highlighting capability
        self.load_button = tk.Button(self.button_frame, text="Load", command=self.load_image,
                                     width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.load_button.pack(side="left", padx=2, pady=2)

        self.bw_button = tk.Button(self.button_frame, text="B&W", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_bw_filter, self.bw_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.bw_button.pack(side="left", padx=2, pady=2)

        self.vivid_cool_button = tk.Button(self.button_frame, text="Vivid", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_vivid_cool_filter, self.vivid_cool_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.vivid_cool_button.pack(side="left", padx=2, pady=2)

        self.retro_button = tk.Button(self.button_frame, text="Retro", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_retro_filter, self.retro_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.retro_button.pack(side="left", padx=2, pady=2)

        self.sepia_button = tk.Button(self.button_frame, text="Sepia", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_sepia_filter, self.sepia_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.sepia_button.pack(side="left", padx=2, pady=2)

        self.warm_glow_button = tk.Button(self.button_frame, text="Warm", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_warm_glow_filter, self.warm_glow_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.warm_glow_button.pack(side="left", padx=2, pady=2)

        self.sharpen_button = tk.Button(self.button_frame, text="Sharp", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_sharpen_filter, self.sharpen_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.sharpen_button.pack(side="left", padx=2, pady=2)

        self.high_contrast_button = tk.Button(self.button_frame, text="Contrast", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_high_contrast_filter, self.high_contrast_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.high_contrast_button.pack(side="left", padx=2, pady=2)

        self.pencil_sketch_button = tk.Button(self.button_frame, text="Sketch", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_pencil_sketch_filter, self.pencil_sketch_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.pencil_sketch_button.pack(side="left", padx=2, pady=2)

        self.blur_button = tk.Button(self.button_frame, text="Blur", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_blur_filter, self.blur_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.blur_button.pack(side="left", padx=2, pady=2)

        self.vintage_polaroid_button = tk.Button(self.button_frame, text="Polaroid", command=lambda: self.apply_filter_with_timer_and_highlight(
            self.apply_vintage_polaroid_filter, self.vintage_polaroid_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.vintage_polaroid_button.pack(side="left", padx=2, pady=2)

        self.rotate_button = tk.Button(self.button_frame, text="Rotate", command=lambda: self.apply_rotation_with_highlight(
            self.rotate_image, self.rotate_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.rotate_button.pack(side="left", padx=2, pady=2)

        self.save_button = tk.Button(self.button_frame, text="Save", command=lambda: self.apply_save_with_highlight(
            self.save_image, self.save_button), state="disabled", width=8, height=2, font=("Arial", 8), relief="raised", borderwidth=2)
        self.save_button.pack(side="left", padx=2, pady=2)

        # Labels to display the original and processed images
        self.original_image_label = tk.Label(self.left_frame)
        self.original_image_label.pack(pady=20)

        self.processed_image_label = tk.Label(self.right_frame)
        self.processed_image_label.pack(pady=20)

        # Labels for image descriptions with dynamic bolding
        self.original_label = tk.Label(
            self.left_frame, text="Original", font=("Arial", 12))
        self.original_label.pack(pady=5)

        self.processed_label = tk.Label(
            self.right_frame, text="Processed", font=("Arial", 12))
        self.processed_label.pack(pady=5)

        # Label for processing time (placed below buttons)
        self.processing_time_label = tk.Label(
            root, text="", font=("Arial", 10))
        self.processing_time_label.pack(pady=5)

        # Store the original and processed images
        self.original_image = None
        self.processed_image = None
        self.original_photo = None
        self.processed_photo = None

    def resize_to_fit(self, image, max_size=400):
        """Resize the image to fit within max_size while maintaining aspect ratio."""
        width, height = image.size
        # Calculate the scaling factor based on the longer dimension
        scale = min(max_size / width, max_size / height)
        # Calculate new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)
        # Resize the image
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def resize_for_processing(self, image, max_size=800):
        """Resize the image to fit within max_size for processing while maintaining aspect ratio."""
        width, height = image.size
        # Calculate the scaling factor based on the longer dimension
        scale = min(max_size / width, max_size / height)
        # Calculate new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)
        # Resize the image
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def apply_filter_with_timer_and_highlight(self, filter_function, button):
        """Apply a filter, measure the time taken, update the processing time label, highlight the button, and bold the Processed label."""
        self.highlight_button(button)
        # Reset processed_image to a copy of the original_image before applying the new filter
        self.processed_image = self.original_image.copy()
        start_time = time.time()
        filter_function()
        end_time = time.time()
        processing_time = end_time - start_time
        self.processing_time_label.config(
            text=f"Processing time: {processing_time:.2f} seconds")
        # Bold the Processed label when a filter is applied
        self.processed_label.config(font=("Arial", 12, "bold"))
        # Reset Original to normal
        self.original_label.config(font=("Arial", 12))

    def apply_rotation_with_highlight(self, rotation_function, button):
        """Apply rotation, highlight the button, and bold both labels."""
        self.highlight_button(button)
        start_time = time.time()
        rotation_function()
        end_time = time.time()
        processing_time = end_time - start_time
        self.processing_time_label.config(
            text=f"Processing time: {processing_time:.2f} seconds")
        # Bold both labels when rotating (since rotation affects both images)
        self.original_label.config(font=("Arial", 12, "bold"))
        self.processed_label.config(font=("Arial", 12, "bold"))

    def apply_save_with_highlight(self, save_function, button):
        """Apply save, highlight the button, and bold the Processed label."""
        self.highlight_button(button)
        save_function()
        # Bold the Processed label when saving (since it saves the processed image)
        self.processed_label.config(font=("Arial", 12, "bold"))
        # Reset Original to normal
        self.original_label.config(font=("Arial", 12))

    def highlight_button(self, button):
        """Highlight the selected button by changing its relief and reset the last button."""
        if self.last_button:
            # Reset previous button
            self.last_button.config(relief="raised", borderwidth=2)
        # Highlight current button
        button.config(relief="sunken", borderwidth=4)
        self.last_button = button

    def load_image(self):
        # Open a file dialog to select an image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            # Open the image with PIL
            self.original_image = Image.open(file_path)
            # Resize to a smaller processing size (e.g., 800x600 max) while maintaining aspect ratio
            self.original_image = self.resize_for_processing(
                self.original_image)
            # Start with a copy for processing
            self.processed_image = self.original_image.copy()
            # Resize for display (400 max) while maintaining aspect ratio
            display_original = self.resize_to_fit(self.original_image)
            display_processed = self.resize_to_fit(self.processed_image)
            # Convert to Tkinter-compatible photos
            self.original_photo = ImageTk.PhotoImage(display_original)
            self.processed_photo = ImageTk.PhotoImage(display_processed)
            self.original_image_label.config(image=self.original_photo)
            self.processed_image_label.config(image=self.processed_photo)
            # Enable all buttons
            self.bw_button.config(state="normal")
            self.vivid_cool_button.config(state="normal")
            self.retro_button.config(state="normal")
            self.sepia_button.config(state="normal")
            self.warm_glow_button.config(state="normal")
            self.sharpen_button.config(state="normal")
            self.high_contrast_button.config(state="normal")
            self.pencil_sketch_button.config(state="normal")
            self.blur_button.config(state="normal")
            self.vintage_polaroid_button.config(state="normal")
            self.rotate_button.config(state="normal")
            self.save_button.config(state="normal")

    def apply_bw_filter(self):
        if self.processed_image:
            # Convert the processed image to grayscale (black and white)
            bw_image = self.processed_image.convert(
                'L')  # 'L' mode is grayscale
            # Resize for display while maintaining aspect ratio
            display_bw = self.resize_to_fit(bw_image)
            self.processed_photo = ImageTk.PhotoImage(display_bw)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version (for saving and further edits)
            self.processed_image = bw_image

    def apply_vivid_cool_filter(self):
        if self.processed_image:
            # Convert to RGB and NumPy array
            if self.processed_image.mode != 'RGB':
                rgb_image = self.processed_image.convert('RGB')
            else:
                rgb_image = self.processed_image
            np_image = np.array(rgb_image, dtype=np.uint8)

            # Apply Vivid Cool filter using NumPy: enhance blues, reduce reds/yellows
            r, g, b = np_image[..., 0], np_image[..., 1], np_image[..., 2]
            # Reduce red slightly
            new_r = np.clip(r * 0.7, 0, 255).astype(np.uint8)
            # Slightly boost green
            new_g = np.clip(g * 1.1, 0, 255).astype(np.uint8)
            # Boost blue for a cool effect
            new_b = np.clip(b * 1.3, 0, 255).astype(np.uint8)
            np_image[..., 0] = new_r
            np_image[..., 1] = new_g
            np_image[..., 2] = new_b

            # Convert back to PIL Image
            vivid_image = Image.fromarray(np_image)
            # Resize for display while maintaining aspect ratio
            display_vivid = self.resize_to_fit(vivid_image)
            self.processed_photo = ImageTk.PhotoImage(display_vivid)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = vivid_image

    def apply_retro_filter(self):
        if self.processed_image:
            # Convert to RGB and NumPy array
            if self.processed_image.mode != 'RGB':
                rgb_image = self.processed_image.convert('RGB')
            else:
                rgb_image = self.processed_image
            np_image = np.array(rgb_image, dtype=np.uint8)

            # Apply Retro filter: muted colors with a slight sepia effect
            r, g, b = np_image[..., 0], np_image[..., 1], np_image[..., 2]
            # Sepia transformation
            tr = np.clip(0.393 * r + 0.769 * g + 0.189 *
                         b, 0, 255).astype(np.uint8)
            tg = np.clip(0.349 * r + 0.686 * g + 0.168 *
                         b, 0, 255).astype(np.uint8)
            tb = np.clip(0.272 * r + 0.534 * g + 0.131 *
                         b, 0, 255).astype(np.uint8)
            # Reduce saturation for a retro look (average grayscale)
            avg = (r + g + b) // 3
            new_r = np.clip((tr * 0.6 + avg * 0.4), 0, 255).astype(np.uint8)
            new_g = np.clip((tg * 0.6 + avg * 0.4), 0, 255).astype(np.uint8)
            new_b = np.clip((tb * 0.6 + avg * 0.4), 0, 255).astype(np.uint8)
            np_image[..., 0] = new_r
            np_image[..., 1] = new_g
            np_image[..., 2] = new_b

            # Convert back to PIL Image
            retro_image = Image.fromarray(np_image)
            # Resize for display while maintaining aspect ratio
            display_retro = self.resize_to_fit(retro_image)
            self.processed_photo = ImageTk.PhotoImage(display_retro)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = retro_image

    def apply_sepia_filter(self):
        if self.processed_image:
            # Convert to RGB and NumPy array
            if self.processed_image.mode != 'RGB':
                rgb_image = self.processed_image.convert('RGB')
            else:
                rgb_image = self.processed_image
            np_image = np.array(rgb_image, dtype=np.uint8)

            # Apply sepia effect using NumPy
            r, g, b = np_image[..., 0], np_image[..., 1], np_image[..., 2]
            tr = np.clip(0.393 * r + 0.769 * g + 0.189 *
                         b, 0, 255).astype(np.uint8)
            tg = np.clip(0.349 * r + 0.686 * g + 0.168 *
                         b, 0, 255).astype(np.uint8)
            tb = np.clip(0.272 * r + 0.534 * g + 0.131 *
                         b, 0, 255).astype(np.uint8)
            np_image[..., 0] = tr
            np_image[..., 1] = tg
            np_image[..., 2] = tb

            # Convert back to PIL Image
            sepia_image = Image.fromarray(np_image)
            # Resize for display while maintaining aspect ratio
            display_sepia = self.resize_to_fit(sepia_image)
            self.processed_photo = ImageTk.PhotoImage(display_sepia)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = sepia_image

    def apply_warm_glow_filter(self):
        if self.processed_image:
            # Convert to RGB and NumPy array
            if self.processed_image.mode != 'RGB':
                rgb_image = self.processed_image.convert('RGB')
            else:
                rgb_image = self.processed_image
            np_image = np.array(rgb_image, dtype=np.uint8)

            # Apply Warm Glow filter using NumPy: enhance reds and yellows, reduce blues
            r, g, b = np_image[..., 0], np_image[..., 1], np_image[..., 2]
            # Increase red slightly
            new_r = np.clip(r * 1.2, 0, 255).astype(np.uint8)
            # Slightly boost green
            new_g = np.clip(g * 1.1, 0, 255).astype(np.uint8)
            new_b = np.clip(b * 0.8, 0, 255).astype(np.uint8)    # Reduce blue
            np_image[..., 0] = new_r
            np_image[..., 1] = new_g
            np_image[..., 2] = new_b

            # Convert back to PIL Image
            warm_image = Image.fromarray(np_image)
            # Resize for display while maintaining aspect ratio
            display_warm = self.resize_to_fit(warm_image)
            self.processed_photo = ImageTk.PhotoImage(display_warm)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = warm_image

    def apply_sharpen_filter(self):
        if self.processed_image:
            # Apply sharpen filter using PIL's built-in filter
            sharpened_image = self.processed_image.filter(ImageFilter.SHARPEN)
            # Resize for display while maintaining aspect ratio
            display_sharpened = self.resize_to_fit(sharpened_image)
            self.processed_photo = ImageTk.PhotoImage(display_sharpened)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = sharpened_image

    def apply_high_contrast_filter(self):
        if self.processed_image:
            # Convert to RGB if not already
            if self.processed_image.mode != 'RGB':
                rgb_image = self.processed_image.convert('RGB')
            else:
                rgb_image = self.processed_image

            # Apply high contrast by enhancing contrast (factor of 2.0)
            enhancer = ImageEnhance.Contrast(rgb_image)
            # Increase contrast by a factor of 2
            contrast_image = enhancer.enhance(2.0)
            # Resize for display while maintaining aspect ratio
            display_contrast = self.resize_to_fit(contrast_image)
            self.processed_photo = ImageTk.PhotoImage(display_contrast)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = contrast_image

    def apply_pencil_sketch_filter(self):
        if self.processed_image:
            # Convert to grayscale
            bw_image = self.processed_image.convert('L')
            # Invert and blur using PIL filters
            inverted = bw_image.point(lambda x: 255 - x)
            blurred = inverted.filter(ImageFilter.GaussianBlur(radius=2))
            # Blend using PIL's blend
            sketch = Image.blend(bw_image, blurred, alpha=0.7)
            # Resize for display while maintaining aspect ratio
            display_sketch = self.resize_to_fit(sketch)
            self.processed_photo = ImageTk.PhotoImage(display_sketch)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = sketch

    def apply_blur_filter(self):
        if self.processed_image:
            # Apply Gaussian blur with a radius of 2
            blurred_image = self.processed_image.filter(
                ImageFilter.GaussianBlur(radius=2))
            # Resize for display while maintaining aspect ratio
            display_blurred = self.resize_to_fit(blurred_image)
            self.processed_photo = ImageTk.PhotoImage(display_blurred)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = blurred_image

    def apply_vintage_polaroid_filter(self):
        if self.processed_image:
            # Convert to RGB and NumPy array
            if self.processed_image.mode != 'RGB':
                rgb_image = self.processed_image.convert('RGB')
            else:
                rgb_image = self.processed_image
            np_image = np.array(rgb_image, dtype=np.uint8)

            # Apply retro effect (similar to sepia but muted) using NumPy
            r, g, b = np_image[..., 0], np_image[..., 1], np_image[..., 2]
            tr = np.clip(0.393 * r + 0.769 * g + 0.189 *
                         b, 0, 255).astype(np.uint8)
            tg = np.clip(0.349 * r + 0.686 * g + 0.168 *
                         b, 0, 255).astype(np.uint8)
            tb = np.clip(0.272 * r + 0.534 * g + 0.131 *
                         b, 0, 255).astype(np.uint8)
            avg = (r + g + b) // 3
            new_r = np.clip((tr * 0.7 + avg * 0.3), 0, 255).astype(np.uint8)
            new_g = np.clip((tg * 0.7 + avg * 0.3), 0, 255).astype(np.uint8)
            new_b = np.clip((tb * 0.7 + avg * 0.3), 0, 255).astype(np.uint8)
            np_image[..., 0] = new_r
            np_image[..., 1] = new_g
            np_image[..., 2] = new_b

            # Convert back to PIL Image
            vintage_image = Image.fromarray(np_image)
            # Apply slight blur for soft edges
            vintage_image = vintage_image.filter(
                ImageFilter.GaussianBlur(radius=0.5))

            # Optional: Add a faded border (e.g., light yellow)
            width, height = vintage_image.size
            border_width = 10
            bordered_image = Image.new(
                "RGB", (width + 2 * border_width, height + 2 * border_width), (245, 220, 180))  # Light yellow border
            bordered_image.paste(vintage_image, (border_width, border_width))
            vintage_image = bordered_image

            # Resize for display while maintaining aspect ratio
            display_vintage = self.resize_to_fit(vintage_image)
            self.processed_photo = ImageTk.PhotoImage(display_vintage)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = vintage_image

    def rotate_image(self):
        if self.original_image and self.processed_image:
            # Rotate both the original and processed images 90 degrees clockwise
            # expand=True ensures the full rotated image fits
            self.original_image = self.resize_for_processing(
                self.original_image.rotate(-90, expand=True))
            # Apply the same rotation to the processed image
            self.processed_image = self.resize_for_processing(
                self.processed_image.rotate(-90, expand=True))
            # Resize both for display while maintaining aspect ratio
            display_original = self.resize_to_fit(self.original_image)
            display_processed = self.resize_to_fit(self.processed_image)
            # Convert to Tkinter-compatible photos
            self.original_photo = ImageTk.PhotoImage(display_original)
            self.processed_photo = ImageTk.PhotoImage(display_processed)
            self.original_image_label.config(image=self.original_photo)
            self.processed_image_label.config(image=self.processed_photo)

    def save_image(self):
        if self.processed_image:
            # Open a file dialog to save the processed image
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
                                                     ("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                self.processed_image.save(save_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFilterApp(root)
    root.mainloop()
