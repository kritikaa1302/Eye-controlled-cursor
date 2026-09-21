# 👁️ Eye Controlled Cursor

Control your mouse cursor with your eyes using just a webcam. Move your eyes to move the cursor, and blink to click.

Built with **OpenCV**, **MediaPipe Face Mesh** and **PyAutoGUI**.

## Features

- Cursor follows your iris in real time, with smoothing to reduce jitter
- Click by blinking both eyes (or winking one eye for left/right click)
- Deliberate-blink detection, so normal blinks don't cause accidental clicks
- Cursor freezes while your eyes are closed, so it doesn't jump when you click
- Live preview showing eye-openness values for easy tuning
- Quit with `q`, `Ctrl+C`, or by moving the cursor to a screen corner

## Requirements

- Python 3.9 to 3.12
- A webcam

```bash
pip install opencv-python mediapipe==0.10.14 pyautogui
```

> MediaPipe `0.10.14` is required. Newer versions removed the `mp.solutions` API this project uses.

## Usage

```bash
python eye_mouse.py
```

| Action | Result |
|---|---|
| Move your eyes | Moves the cursor |
| Close both eyes for ~0.4 s (`blink` mode) | Left click |
| Close left / right eye (`wink` mode) | Left / right click |
| Press `q` in the webcam window | Quit |

## Settings

Edit these at the top of `eye_mouse.py`:

| Setting | Default | Description |
|---|---|---|
| `CLICK_MODE` | `"blink"` | `"blink"` = both eyes to left-click, `"wink"` = one eye per click type |
| `HOLD_TIME` | `0.4` | Seconds eyes must stay closed to click |
| `BLINK_RATIO` | `0.18` | Eye counts as closed below this value (lower = harder to click) |
| `SMOOTHING` | `0.3` | Lower = smoother but slower cursor |
| `CAMERA_INDEX` | `0` | Use `1` if the wrong camera or a black window appears |

**Tip:** the on-screen `L:` and `R:` numbers show how open each eye is. Set `BLINK_RATIO` between your open and closed values.

## Troubleshooting

- **`module 'mediapipe' has no attribute 'solutions'`**: run `pip install mediapipe==0.10.14` and use Python 3.9 to 3.12.
- **Clicks too often or never**: adjust `BLINK_RATIO` or `HOLD_TIME`.
- **Jittery cursor**: lower `SMOOTHING` and use bright, even lighting.
- **macOS**: allow camera and accessibility access for your terminal or VS Code.

## Tech Stack

Python, OpenCV, MediaPipe, PyAutoGUI
