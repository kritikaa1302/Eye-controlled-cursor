import cv2
import mediapipe as mp
import pyautogui

# ---------------- Settings ----------------
SMOOTHING = 0.3          # 0 = very smooth/slow, 1 = no smoothing (raw, jittery)
BLINK_THRESHOLD = 0.004  # smaller = you must close your eye more to click
CLICK_DELAY = 1          # seconds to wait after a click
CAMERA_INDEX = 0         # try 1 if the window is black
# ------------------------------------------

pyautogui.PAUSE = 0      # remove the default delay after each pyautogui call

cam = cv2.VideoCapture(CAMERA_INDEX)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

prev_x, prev_y = screen_w / 2, screen_h / 2

try:
    while True:
        ok, frame = cam.read()
        if not ok:
            print("Could not read from camera. Check CAMERA_INDEX or permissions.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark

            # Iris landmarks (474-477) -> move the cursor
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))

                if id == 1:
                    target_x = screen_w * landmark.x
                    target_y = screen_h * landmark.y

                    # Smooth the movement
                    prev_x = prev_x + (target_x - prev_x) * SMOOTHING
                    prev_y = prev_y + (target_y - prev_y) * SMOOTHING
                    pyautogui.moveTo(prev_x, prev_y)

            # Left eye landmarks (145 = bottom lid, 159 = top lid) -> blink to click
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

            if (left[0].y - left[1].y) < BLINK_THRESHOLD:
                pyautogui.click()
                pyautogui.sleep(CLICK_DELAY)

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