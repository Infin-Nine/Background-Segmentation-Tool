# Background Segmentation Tool

A professional Python-based GUI application that uses **MediaPipe's Selfie Segmenter** to perform real-time image background manipulation.

## Features
* **Remove Background:** Isolates the subject and removes the background.
* **Green Screen:** Replaces the background with a standard chroma key green.
* **Change Background:** Allows users to upload a custom image as a new background.

## Tech Stack
* **Core:** Python, OpenCV, MediaPipe (Task API)
* **GUI:** Tkinter
* **Imaging:** Pillow, NumPy

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

    <img width="400" height="350" alt="Screenshot 2026-02-02 150533" src="https://github.com/user-attachments/assets/9994db56-f410-49ee-bca3-cdc17d74d4fa" />
    <img width="400" height="350" alt="Screenshot 2026-02-02 150557" src="https://github.com/user-attachments/assets/7198a158-cb0b-421b-9fd1-d92895d7279e" />
    <img width="400" height="350" alt="Screenshot 2026-02-02 150610" src="https://github.com/user-attachments/assets/2ab0cc33-1d17-4aaa-a5e4-930fd49d7d71" />


    

