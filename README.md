# Background Removal Tool

A Python-based GUI application that uses **MediaPipe's Selfie Segmenter** to perform real-time image and video background manipulation.

## Features
* **Single Image Processing:** Remove backgrounds, apply a Green Screen, or replace with a custom background image.
* **Live Video Mode:** Real-time background removal using your webcam with low latency.
* **Batch Processing:** Process multiple images at once and save them automatically to a dedicated folder.
* **Professional UI:** Modern and sleek dark-themed interface built with `ttkbootstrap`.
* **Export Ready:** Instantly save your processed images in PNG or JPG format.

## Tech Stack
* **Core:** Python, OpenCV, MediaPipe (Task API)
* **GUI:** Tkinter
* **Imaging:** Pillow, NumPy
* **Dark-Theme-Interface:** ttkbootstrap

## How it Works
This tool is powered by the **MediaPipe Selfie Segmenter** model. 

* **Person-Centric Design:** The underlying machine learning model is specifically trained to recognize and isolate human features. 
* **Optimal Performance:** For the best results, ensure the input image contains a clear view of a person. The tool excels at identifying human contours and separating them from complex backgrounds.
* **Limitations:** Since it is a "Selfie" model, it may not perform accurately on images of animals, inanimate objects, or landscapes without a human subject.

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Infin-Nine/Background-Segmentation-Tool.git
    cd Background-Segmentation-Tool
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Model Placement:**
    Place the `selfie_segmenter.tflite` model inside the `Models/` directory.

4.  **Run the App:**
    ```bash
    python main.py
    ```

<<<<<<< HEAD



    

=======
    <img width="1100" height="735" alt="Screenshot 2026-02-02 160916" src="https://github.com/user-attachments/assets/f880b280-8c74-4aa6-a725-bef48dbaf35d" />
>>>>>>> 913ca08074fe93dee5580d0d858d35f80f718607
