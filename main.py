import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


# ================== CONFIG ==================
MODEL_PATH = "selfie_segmenter.tflite"

# ================== MODEL ==================
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options_img = vision.ImageSegmenterOptions(
    base_options=base_options,
    output_category_mask=True,
    running_mode=vision.RunningMode.IMAGE
)

options_vid = vision.ImageSegmenterOptions(
    base_options=base_options,
    output_category_mask=True,
    running_mode=vision.RunningMode.VIDEO
)


def segment_core(image, mode, bg_img=None):
    h, w = image.shape[:2]

    with vision.ImageSegmenter.create_from_options(options_img) as segmenter:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(mp.ImageFormat.SRGB, data=rgb)

        result = segmenter.segment(mp_image)
        category_mask = result.category_mask.numpy_view()

        mask = np.where(category_mask < 0.1, 255, 0).astype(np.uint8)
        # mask = smooth_mask(mask)
        inv = cv2.bitwise_not(mask)

        person = cv2.bitwise_and(image, image, mask=mask)

        if mode == "Remove BG":
            return person

        if mode == "Green BG":
            green = np.zeros_like(image)
            green[:] = (0, 255, 0)
            bg = cv2.bitwise_and(green, green, mask=inv)
            return cv2.add(person, bg)

        if mode == "Change BG":
            bg_img = cv2.resize(bg_img, (w, h))
            bg = cv2.bitwise_and(bg_img, bg_img, mask=inv)
            return cv2.add(person, bg)

# ================== APP ==================
class SegmentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Professional MediaPipe Segmentation Tool")
        self.root.geometry("1100x700")

        self.image = None
        self.bg_image = None
        self.last_output = None

        # -------- UI --------
        tb.Label(root, text="Background Removal Toolkit",
                 font=("Segoe UI", 22, "bold")).pack(pady=10)

        self.mode = tb.StringVar(value="Remove BG")
        tb.OptionMenu(root, self.mode,
                      "Remove BG", "Remove BG",
                      "Green BG", "Change BG").pack(pady=5)

        btn_frame = tb.Frame(root)
        btn_frame.pack(pady=10)

        tb.Button(btn_frame, text="Load Image", command=self.load_image).grid(row=0, column=0, padx=5)
        tb.Button(btn_frame, text="Load Background", command=self.load_bg).grid(row=0, column=1, padx=5)
        tb.Button(btn_frame, text="Process Image", command=self.process).grid(row=0, column=2, padx=5)
        tb.Button(btn_frame, text="Export", command=self.export).grid(row=0, column=3, padx=5)
        tb.Button(btn_frame, text="Batch Mode", command=self.batch).grid(row=0, column=4, padx=5)
        tb.Button(btn_frame, text="Video Mode", command=self.video_mode).grid(row=0, column=5, padx=5)

        self.preview = tb.Label(root)
        self.preview.pack(pady=20)

    # -------- FUNCTIONS --------
    def show(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        pil.thumbnail((700, 450))
        self.tk_img = ImageTk.PhotoImage(pil)
        self.preview.config(image=self.tk_img)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if not path:
            return
        self.image = cv2.imread(path)
        if self.image is None:
            messagebox.showerror("Error", "Invalid image")
            return
        self.show(self.image)

    def load_bg(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if not path:
            return
        self.bg_image = cv2.imread(path)

    def process(self):
        if self.image is None:
            messagebox.showwarning("Warning", "Load image first")
            return
        if self.mode.get() == "Change BG" and self.bg_image is None:
            messagebox.showwarning("Warning", "Load background image")
            return

        self.last_output = segment_core(self.image, self.mode.get(), self.bg_image)
        self.show(self.last_output)

    def export(self):
        if self.last_output is None:
            messagebox.showwarning("Warning", "Nothing to export")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")])
        if path:
            cv2.imwrite(path, self.last_output)
            messagebox.showinfo("Saved", "Image exported")

    def batch(self):
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if not paths:
            return

        out_dir = "batch_output"
        os.makedirs(out_dir, exist_ok=True)

        for p in paths:
            img = cv2.imread(p)
            if img is None:
                continue
            out = segment_core(img, self.mode.get(), self.bg_image)
            cv2.imwrite(os.path.join(out_dir, os.path.basename(p)), out)

        messagebox.showinfo("Done", "Batch processing complete")

    def video_mode(self):
        cap = cv2.VideoCapture(0)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_id = 0

        with vision.ImageSegmenter.create_from_options(options_vid) as segmenter:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_img = mp.Image(mp.ImageFormat.SRGB, rgb)
                ts = int((frame_id / fps) * 1000)
                frame_id += 1

                result = segmenter.segment_for_video(mp_img, ts)
                mask = np.where(result.category_mask.numpy_view() < 0.1, 255, 0).astype(np.uint8)
                # mask = smooth_mask(mask)
                inv = cv2.bitwise_not(mask)

                person = cv2.bitwise_and(frame, frame, mask=mask)

                if self.mode.get() == "Green BG":
                    green = np.zeros_like(frame)
                    green[:] = (0, 255, 0)
                    bg = cv2.bitwise_and(green, green, mask=inv)
                    out = cv2.add(person, bg)
                else:
                    out = person

                cv2.imshow("Video Segmentation", out)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        cap.release()
        cv2.destroyAllWindows()

# ================== RUN ==================
if __name__ == "__main__":
    if not os.path.exists(MODEL_PATH):
        messagebox.showerror("Error", "Model not found")
    else:
        app = tb.Window(themename="darkly")
        SegmentationApp(app)
        app.mainloop()