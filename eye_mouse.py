import math
import time

import cv2
import mediapipe as mp
import pyautogui

# ---------------- Settings ----------------
CLICK_MODE = "blink"     # "blink" = close BOTH eyes -> left click
                         # "wink"  = close ONE eye: left eye -> left click, right eye -> right click
HOLD_TIME = 0.4          # seconds the eye(s) must stay closed to click (filters natural blinks)
BLINK_RATIO = 0.18       # eye is "closed" below this openness ratio (see numbers on screen to tune)
SMOOTHING = 0.3          # 0 = very smooth/slow, 1 = raw/jittery
CAMERA_INDEX = 0         # try 1 if the window is black
# ------------------------------------------

pyautogui.PAUSE = 0

# Eye landmark indices: (top lid, bottom lid, outer corner, inner corner)
LEFT_EYE = (159, 145, 33, 133)     # eye on the left side of the mirrored preview
RIGHT_EYE = (386, 374, 362, 263)   # eye on the right side of the mirrored preview


def eye_ratio(landmarks, idx, w, h):
    """Eye openness = lid gap / eye width. Open is ~0.25-0.35, closed is below ~0.15."""
    top, bottom, corner_a, corner_b = (landmarks[i] for i in idx)
    vertical = math.hypot((top.x - bottom.x) * w, (top.y - bottom.y) * h)
    horizontal = math.hypot((corner_a.x - corner_b.x) * w, (corner_a.y - corner_b.y) * h)
    return vertical / horizontal if horizontal else 1.0


cam = cv2.VideoCapture(CAMERA_INDEX)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

prev_x, prev_y = screen_w / 2, screen_h / 2
current_action = None    # "left", "right" or None
action_start = 0.0
fired = False            # so one long blink gives only one click

try:
    while True:
        ok, frame = cam.read()
        if not ok:
            print("Could not read from camera. Check CAMERA_INDEX or permissions.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        frame_h, frame_w, _ = frame.shape

        if output.multi_face_landmarks:
            landmarks = output.multi_face_landmarks[0].landmark

            left_ratio = eye_ratio(landmarks, LEFT_EYE, frame_w, frame_h)
            right_ratio = eye_ratio(landmarks, RIGHT_EYE, frame_w, frame_h)
            left_closed = left_ratio < BLINK_RATIO
            right_closed = right_ratio < BLINK_RATIO

            # Draw iris points and eyelid points
            for lm in landmarks[474:478]:
                cv2.circle(frame, (int(lm.x * frame_w), int(lm.y * frame_h)), 3, (0, 255, 0))
            for idx in (LEFT_EYE, RIGHT_EYE):
                for i in idx[:2]:
                    lm = landmarks[i]
                    cv2.circle(frame, (int(lm.x * frame_w), int(lm.y * frame_h)), 3, (0, 255, 255))

            # Move the cursor only while both eyes are open
            # (closing your eyes shifts the iris and would make the cursor jump)
            if not (left_closed or right_closed):
                iris = landmarks[475]
                target_x = screen_w * iris.x
                target_y = screen_h * iris.y
                prev_x += (target_x - prev_x) * SMOOTHING
                prev_y += (target_y - prev_y) * SMOOTHING
                pyautogui.moveTo(prev_x, prev_y)

            # Decide which click (if any) the current eye state means
            action = None
            if CLICK_MODE == "blink":
                if left_closed and right_closed:
                    action = "left"
            else:  # wink
                if left_closed and not right_closed:
                    action = "left"
                elif right_closed and not left_closed:
                    action = "right"

            # Click once the eye(s) have stayed closed for HOLD_TIME
            now = time.time()
            if action != current_action:
                current_action = action
                action_start = now
                fired = False
            if action and not fired and now - action_start >= HOLD_TIME:
                pyautogui.click(button=action)
                fired = True

            # On-screen numbers to help you tune BLINK_RATIO
            cv2.putText(frame, f"L:{left_ratio:.2f} R:{right_ratio:.2f} (closed < {BLINK_RATIO})",
                        (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Mode: {CLICK_MODE}   q = quit",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            if fired:
                cv2.putText(frame, "CLICK!", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow('Eye Controlled Mouse', frame)

        # Press 'q' (with the webcam window focused) to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except pyautogui.FailSafeException:
    print("Failsafe triggered (cursor hit a screen corner). Stopping.")
except KeyboardInterrupt:
    print("Stopped with Ctrl+C.")
finally:
    cam.release()
    cv2.destroyAllWindows()
    face_mesh.close()