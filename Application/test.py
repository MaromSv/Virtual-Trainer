import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from pushupCounter import pushUpCounter


class VideoApp:
    def __init__(self, root, image_generator):
        self.root = root
        self.image_generator = image_generator
        self.video_canvas = tk.Canvas(root)
        self.video_canvas.pack()

        self.photo = None  # Store PhotoImage as a class attribute

        self.root.after(100, self.update_video)
        self.root.mainloop()

    def update_video(self):
        try:
            image = next(self.image_generator)
            self.display_image(image)
            self.root.after(100, self.update_video)
        except StopIteration:
            # Image sequence is complete
            pass

    def display_image(self, image):
        # Ensure the image is in the correct format and range
        image = np.clip(image, 0, 255).astype(np.uint8)

        # Ensure correct color channels and data type
        if image.shape[-1] != 3:
            raise ValueError("Image should have 3 color channels (RGB)")

        # Convert the NumPy array to a PIL Image and ensure RGB mode
        pil_image = Image.fromarray(image, mode="RGB")

        # Convert the PIL Image to PhotoImage format
        self.photo = ImageTk.PhotoImage(image=pil_image)

        # Update the canvas with the new image
        self.video_canvas.config(width=self.photo.width(), height=self.photo.height())
        self.video_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Keep a reference to the PhotoImage to prevent garbage collection
        self.video_canvas.photo = self.photo

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root,  app = VideoApp(root, pushUpCounter()))
