# Eye-controlled-cursor
Eye Controlled Mouse

Control your computer's mouse cursor with your eyes using a regular webcam. The project uses MediaPipe Face Mesh to track your iris and PyAutoGUI to move the cursor. Blink your left eye to click.

Features
Cursor follows your eye (iris) movement in real time
Blink your left eye to left-click
Smooth cursor movement to reduce jitter
Live webcam preview with tracked landmarks drawn on screen
Clean exit with a quit key
Adjustable settings for smoothing and blink sensitivity
How It Works
OpenCV captures frames from your webcam.
MediaPipe Face Mesh (with refine_landmarks=True) detects 478 face landmarks, including the iris.
The iris position (landmarks 474–477) is mapped to your screen size, and PyAutoGUI moves the cursor there.
The distance between the upper and lower eyelid of the left eye (landmarks 159 and 145) is measured. When it falls below a threshold, the script registers a blink and clicks.
Requirements
Python 3.9 – 3.12
A working webcam
Libraries:
opencv-python
mediapipe==0.10.14
pyautogui

Note: Newer MediaPipe versions removed the mp.solutions API this project uses. Please install version 0.10.14 as shown below.

Installation
Clone the repository:
bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
(Recommended) Create and activate a virtual environment:
bash
   # Windows
   py -3.12 -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
Install the dependencies:
bash
   pip install opencv-python mediapipe==0.10.14 pyautogui
Usage

Run the script:

bash
python eye_mouse.py

A window titled Eye Controlled Mouse will open. Look around to move the cursor, and blink your left eye to click.

Controls
Action	Result
Move your eyes	Moves the cursor
Blink left eye	Left click
Press q (webcam window focused)	Quit the program
Ctrl + C in the terminal	Quit the program
Move the cursor to a screen corner	PyAutoGUI failsafe stops the program
Configuration

Edit the settings at the top of eye_mouse.py:

Setting	Default	Description
SMOOTHING	0.3	Lower = smoother but slower cursor. 1 = no smoothing.
BLINK_THRESHOLD	0.004	Lower = you must close your eye more to click.
CLICK_DELAY	1	Seconds to wait after each click.
CAMERA_INDEX	0	Change to 1 if the wrong camera or a black window appears.
Troubleshooting

AttributeError: module 'mediapipe' has no attribute 'solutions' Install the compatible version and make sure you're on Python 3.9–3.12:

bash
pip uninstall mediapipe -y
pip install mediapipe==0.10.14

Also check that no file in your project is named mediapipe.py or cv2.py.

Black or blank webcam window Set CAMERA_INDEX = 1 (or another number) in the script, and close other apps that may be using the camera.

Cursor doesn't move on macOS Grant camera and accessibility permissions to your terminal or VS Code in System Settings → Privacy & Security.

Cursor is jittery Lower the SMOOTHING value, use good lighting, and keep your head fairly steady.

Clicks happen too often or never happen Adjust BLINK_THRESHOLD up or down in small steps (for example 0.003 to 0.006).

Tips for Best Results
Use bright, even lighting on your face.
Sit facing the camera at a comfortable distance.
Keep your head relatively still and move mainly your eyes.
Limitations
Accuracy depends on webcam quality and lighting.
Only the left eye is used for clicking, and there is no right-click or double-click yet.
Not designed for multi-monitor setups.
Ideas for Future Improvements
Right-click and double-click gestures
Calibration step for better accuracy
Multi-monitor support
Head-pose compensation
Scroll control
Tech Stack
Python
OpenCV
MediaPipe
PyAutoGUI
