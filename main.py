import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# ---------------- MODEL SETUP ----------------
MODEL_PATH = "selfie_segmenter.tflite"

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.ImageSegmenterOptions(
    base_options=base_options,
    output_category_mask=True,
    running_mode=vision.RunningMode.IMAGE
)

# ---------------- SEGMENTATION ENGINE ----------------
def segment_image(image, mode, bg_image=None):
    h, w = image.shape[:2]

    with vision.ImageSegmenter.create_from_options(options) as segmenter:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(mp.ImageFormat.SRGB, data=rgb)

        result = segmenter.segment(mp_image)
        category_mask = result.category_mask.numpy_view()

        mask = np.where(category_mask < 0.1, 255, 0).astype(np.uint8)
        inv_mask = cv2.bitwise_not(mask)

        person = cv2.bitwise_and(image, image, mask=mask)

        if mode == "Remove Background":
            return person

        elif mode == "Green Background":
            green = np.zeros_like(image)
            green[:] = (0, 255, 0)
            bg = cv2.bitwise_and(green, green, mask=inv_mask)
            return cv2.add(person, bg)

        elif mode == "Change Background":
            bg_image = cv2.resize(bg_image, (w, h))
            bg = cv2.bitwise_and(bg_image, bg_image, mask=inv_mask)
            return cv2.add(person, bg)

# ---------------- GUI APP ----------------
class SegmentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Segmentation Tool")
        self.root.geometry("900x600")

        self.image = None
        self.bg_image = None

        # -------- UI ELEMENTS --------
        tk.Label(root, text="Remove Background From Image",
                 font=("Arial", 18, "bold")).pack(pady=10)

        self.mode_var = tk.StringVar(value="Remove Background")

        modes = ["Remove Background", "Green Background", "Change Background"]
        tk.OptionMenu(root, self.mode_var, *modes).pack(pady=5)

        tk.Button(root, text="Select Input Image", command=self.load_image).pack(pady=5)
        tk.Button(root, text="Select Background Image", command=self.load_bg).pack(pady=5)

        tk.Button(root, text="Process Image", command=self.process).pack(pady=10)

        self.canvas = tk.Label(root)
        self.canvas.pack(pady=10)

    # -------- FUNCTIONS --------
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if not path:
            return
        self.image = cv2.imread(path)
        if self.image is None:
            messagebox.showerror("Error", "Invalid image file")
            return
        self.show_image(self.image)

    def load_bg(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if not path:
            return
        self.bg_image = cv2.imread(path)
        if self.bg_image is None:
            messagebox.showerror("Error", "Invalid background image")

    def process(self):
        if self.image is None:
            messagebox.showwarning("Warning", "Please select an input image")
            return

        mode = self.mode_var.get()

        if mode == "Change Background" and self.bg_image is None:
            messagebox.showwarning("Warning", "Please select a background image")
            return

        try:
            output = segment_image(self.image, mode, self.bg_image)
            self.show_image(output)
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

    def show_image(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        pil_img.thumbnail((600, 400))
        self.tk_img = ImageTk.PhotoImage(pil_img)
        self.canvas.config(image=self.tk_img)

# ---------------- RUN ----------------
if __name__ == "__main__":
    if not os.path.exists(MODEL_PATH):
        messagebox.showerror("Model Error", "Segmentation model not found")
    else:
        root = tk.Tk()
        app = SegmentationApp(root)
        root.mainloop()

