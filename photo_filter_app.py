import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class PhotoFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "Photo Filter App - Original and Processed Side by Side")
        # Width increased to accommodate two images side by side
        self.root.geometry("1000x600")

        # Create a frame to hold the original and processed images side by side
        self.content_frame = tk.Frame(root)
        self.content_frame.pack(pady=20, padx=10, fill="both", expand=True)

        # Left frame for the original image (unchanged)
        self.left_frame = tk.Frame(self.content_frame, width=400)
        self.left_frame.pack(side="left", padx=10, fill="both", expand=True)

        # Right frame for the main (processed) image
        self.right_frame = tk.Frame(self.content_frame, width=400)
        self.right_frame.pack(side="right", padx=10, fill="both", expand=True)

        # Create buttons (place them above the images)
        self.load_button = tk.Button(
            root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        self.bw_button = tk.Button(
            root, text="Apply Black & White Filter", command=self.apply_bw_filter, state="disabled")
        self.bw_button.pack(pady=10)

        self.vivid_cool_button = tk.Button(
            root, text="Apply Vivid Cool Filter", command=self.apply_vivid_cool_filter, state="disabled")
        self.vivid_cool_button.pack(pady=10)

        self.retro_button = tk.Button(
            root, text="Apply Retro Filter", command=self.apply_retro_filter, state="disabled")
        self.retro_button.pack(pady=10)

        self.rotate_button = tk.Button(
            root, text="Rotate 90° Clockwise", command=self.rotate_image, state="disabled")
        self.rotate_button.pack(pady=10)

        self.save_button = tk.Button(
            root, text="Save Image", command=self.save_image, state="disabled")
        self.save_button.pack(pady=10)

        # Labels to display the original and processed images
        self.original_image_label = tk.Label(self.left_frame)
        self.original_image_label.pack(pady=20)

        self.processed_image_label = tk.Label(self.right_frame)
        self.processed_image_label.pack(pady=20)

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

    def load_image(self):
        # Open a file dialog to select an image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            # Open the image with PIL
            self.original_image = Image.open(file_path)
            # Start with a copy for processing
            self.processed_image = self.original_image.copy()
            # Resize both for display while maintaining aspect ratio
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
            # Convert to RGB if not already
            if self.processed_image.mode != 'RGB':
                rgb_image = self.processed_image.convert('RGB')
            else:
                rgb_image = self.processed_image

            # Apply Vivid Cool filter: enhance blues, reduce reds/yellows
            width, height = rgb_image.size
            pixels = rgb_image.load()
            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y]
                    # Increase blue and green (cool tones), reduce red (warm tones)
                    new_r = max(0, min(255, r * 0.7))  # Reduce red slightly
                    new_g = max(0, min(255, g * 1.1))  # Slightly boost green
                    # Boost blue for a cool effect
                    new_b = max(0, min(255, b * 1.3))
                    pixels[x, y] = (int(new_r), int(new_g), int(new_b))

            # Resize for display while maintaining aspect ratio
            display_vivid = self.resize_to_fit(rgb_image)
            self.processed_photo = ImageTk.PhotoImage(display_vivid)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = rgb_image

    def apply_retro_filter(self):
        if self.processed_image:
            # Convert to RGB if not already
            if self.processed_image.mode != 'RGB':
                rgb_image = self.processed_image.convert('RGB')
            else:
                rgb_image = self.processed_image

            # Apply Retro filter: muted colors with a slight sepia effect
            width, height = rgb_image.size
            pixels = rgb_image.load()
            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y]
                    # Apply a sepia-like effect with muted saturation
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)  # Sepia red
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)  # Sepia green
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)  # Sepia blue
                    # Reduce saturation for a retro look
                    avg = (r + g + b) // 3
                    new_r = int((tr * 0.6 + avg * 0.4))
                    new_g = int((tg * 0.6 + avg * 0.4))
                    new_b = int((tb * 0.6 + avg * 0.4))
                    pixels[x, y] = (max(0, min(255, new_r)), max(
                        0, min(255, new_g)), max(0, min(255, new_b)))

            # Resize for display while maintaining aspect ratio
            display_retro = self.resize_to_fit(rgb_image)
            self.processed_photo = ImageTk.PhotoImage(display_retro)
            self.processed_image_label.config(image=self.processed_photo)
            # Update the processed_image to the filtered version
            self.processed_image = rgb_image

    def rotate_image(self):
        if self.original_image and self.processed_image:
            # Rotate both the original and processed images 90 degrees clockwise
            # expand=True ensures the full rotated image fits
            self.original_image = self.original_image.rotate(-90, expand=True)
            # Apply the same rotation to the processed image
            self.processed_image = self.processed_image.rotate(
                -90, expand=True)
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
