# AirCanvas – Virtual Drawing Using Hand Gestures

AirCanvas is a computer vision-based project that allows users to draw on a virtual canvas using hand and finger movements in front of a webcam.

The project uses **Python** and **OpenCV** to capture live video, detect hand movement, and convert finger motion into drawing on the screen.

## Features

- Draw in the air using finger movement
- Real-time webcam input
- Hand and finger tracking
- Virtual drawing canvas
- Different drawing colors
- Clear canvas option
- Simple and easy-to-use interface
- No mouse or touch screen required

## Technologies Used

- Python
- OpenCV
- Computer Vision
- NumPy
- Webcam

## How It Works

1. The webcam captures live video.
2. The system detects the user's hand and finger position.
3. Finger coordinates are tracked continuously.
4. The movement of the finger is converted into lines on the virtual canvas.
5. The drawing is displayed on the screen in real time.

## Project Workflow

```text
Webcam Input
     ↓
Video Frame Capture
     ↓
Hand / Finger Detection
     ↓
Finger Position Tracking
     ↓
Coordinate Detection
     ↓
Drawing on Virtual Canvas
     ↓
Display Final Output
```

## Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/AirCanvas.git
```

Open the project folder:

```bash
cd AirCanvas
```

Install the required libraries:

```bash
pip install opencv-python numpy
```

If your project uses MediaPipe, install it using:

```bash
pip install mediapipe
```

## Run the Project

Run the main Python file:

```bash
python main.py
```

Make sure your webcam is connected and camera permission is enabled.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- MediaPipe, if used
- Webcam

## Applications

AirCanvas can be useful for:

- Virtual drawing
- Contactless interaction
- Digital teaching
- Presentation annotation
- Computer vision learning
- Gesture-based applications

## Future Scope

- Add more colors and brush sizes
- Add eraser functionality
- Save drawings as images
- Add gesture-based menu selection
- Improve hand detection accuracy
- Add shape recognition
- Add text recognition
- Develop a more attractive user interface

## Project Purpose

The main purpose of AirCanvas is to demonstrate how computer vision and hand tracking can be used to create a touch-free drawing application.

It provides a simple example of human-computer interaction using a webcam and hand gestures.

## Author

**Harshada Surwase**

Diploma in Computer Science

---

⭐ If you like this project, consider giving the repository a star.
