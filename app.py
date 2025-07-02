import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk


class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.image = None
        self.original_image = None

        # GUI Elements
        self.label = Label(root)
        self.label.pack()

        # Buttons
        Button(root, text="Open Image", command=self.open_image).pack()
        Button(root, text="Capture from Camera", command=self.capture_image).pack()

        # Channel Selection
        self.channel_var = StringVar(value="None")
        OptionMenu(root, self.channel_var, "None", "Red", "Green", "Blue", command=self.show_channel).pack()

        # Variant Functions
        Button(root, text="Show Negative", command=self.show_negative).pack()
        Button(root, text="Increase Brightness", command=self.increase_brightness).pack()
        Button(root, text="Draw Red Circle", command=self.draw_circle).pack()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                self.original_image = cv2.imread(file_path)
                self.image = self.original_image.copy()
                self.display_image()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {e}")

    def capture_image(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise Exception("Camera not available")

            ret, frame = cap.read()
            if ret:
                self.original_image = frame
                self.image = self.original_image.copy()
                self.display_image()
            cap.release()
        except Exception as e:
            messagebox.showerror("Error", f"Could not capture image: {e}")

    def display_image(self):
        if self.image is not None:
            img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.label.config(image=img)
            self.label.image = img

    def show_channel(self, channel):
        if self.original_image is None:
            return

        if channel == "None":
            self.image = self.original_image.copy()
        else:
            b, g, r = cv2.split(self.original_image)
            zeros = np.zeros_like(b)

            if channel == "Red":
                self.image = cv2.merge([zeros, zeros, r])
            elif channel == "Green":
                self.image = cv2.merge([zeros, g, zeros])
            elif channel == "Blue":
                self.image = cv2.merge([b, zeros, zeros])

        self.display_image()

    def show_negative(self):
        if self.original_image is not None:
            self.image = 255 - self.original_image
            self.display_image()

    def increase_brightness(self):
        if self.original_image is not None:
            value = simpledialog.askinteger("Brightness", "Enter brightness value (0-100):", minvalue=0, maxvalue=100)
            if value is not None:
                self.image = cv2.convertScaleAbs(self.original_image, alpha=1, beta=value)
                self.display_image()

    def draw_circle(self):
        if self.original_image is not None:
            x = simpledialog.askinteger("Circle", "Enter X coordinate:", minvalue=0,
                                        maxvalue=self.original_image.shape[1])
            y = simpledialog.askinteger("Circle", "Enter Y coordinate:", minvalue=0,
                                        maxvalue=self.original_image.shape[0])
            radius = simpledialog.askinteger("Circle", "Enter radius:", minvalue=1)

            if x is not None and y is not None and radius is not None:
                self.image = self.original_image.copy()
                cv2.circle(self.image, (x, y), radius, (0, 0, 255), -1)  # Красный круг
                self.display_image()


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()