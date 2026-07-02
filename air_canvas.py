import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import time

# ---------------- HAND SETUP ----------------
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# ---------------- CANVAS ----------------
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

colors = [
    (0, 0, 255),      # RED
    (0, 255, 0),      # GREEN
    (255, 0, 0),      # BLUE
    (0, 255, 255)     # YELLOW (CLEAR button color)
]

brush_color = colors[0]
brush_thickness = 5

xp, yp = 0, 0

history = deque(maxlen=20)

cap = cv2.VideoCapture(0)

# ---------------- FUNCTIONS ----------------
def fingers_up(lm):
    tips = [8, 12, 16, 20]

    fingers = []

    # Thumb
    if lm[4].x < lm[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for tip in tips:
        if lm[tip].y < lm[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def save_image(img):
    filename = f"aircanvas_{int(time.time())}.png"
    cv2.imwrite(filename, img)
    print("Saved:", filename)


# ---------------- MAIN LOOP ----------------
while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for handLms in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                handLms,
                mp_hands.HAND_CONNECTIONS
            )

            lm = handLms.landmark

            x1 = int(lm[8].x * w)
            y1 = int(lm[8].y * h)

            x2 = int(lm[12].x * w)
            y2 = int(lm[12].y * h)

            # 🔴 RED POINTER
            cv2.circle(
                frame,
                (x1, y1),
                12,
                (0, 0, 255),
                cv2.FILLED
            )

            # Coordinates
            cv2.putText(
                frame,
                f"X:{x1} Y:{y1}",
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            finger = fingers_up(lm)

            # SAVE IMAGE
            if sum(finger) == 5:
                save_image(canvas)

            # UNDO
            if finger[0] == 1 and finger[1] == 1 and finger[2] == 0:

                if len(history) > 0:
                    canvas = history.pop()

            # SELECTION MODE
            if finger[1] == 1 and finger[2] == 1:

                xp, yp = 0, 0

                if y1 < 80:

                    if x1 < 160:
                        brush_color = colors[0]

                    elif x1 < 320:
                        brush_color = colors[1]

                    elif x1 < 480:
                        brush_color = colors[2]

                    else:
                        canvas = np.zeros(
                            (480, 640, 3),
                            dtype=np.uint8
                        )

                        history.clear()

            # DRAW MODE
            elif finger[1] == 1 and finger[2] == 0:

                cv2.circle(
                    frame,
                    (x1, y1),
                    8,
                    brush_color,
                    -1
                )

                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                history.append(canvas.copy())

                cv2.line(
                    canvas,
                    (xp, yp),
                    (x1, y1),
                    brush_color,
                    brush_thickness
                )

                xp, yp = x1, y1

            else:
                xp, yp = 0, 0

    # ---------------- MERGE ----------------
    gray = cv2.cvtColor(
        canvas,
        cv2.COLOR_BGR2GRAY
    )

    _, inv = cv2.threshold(
        gray,
        50,
        255,
        cv2.THRESH_BINARY_INV
    )

    inv = cv2.cvtColor(
        inv,
        cv2.COLOR_GRAY2BGR
    )

    frame = cv2.bitwise_and(
        frame,
        inv
    )

    frame = cv2.bitwise_or(
        frame,
        canvas
    )

    # ---------------- UI ----------------
    cv2.rectangle(frame, (0, 0), (160, 80), colors[0], -1)
    cv2.rectangle(frame, (160, 0), (320, 80), colors[1], -1)
    cv2.rectangle(frame, (320, 0), (480, 80), colors[2], -1)
    cv2.rectangle(frame, (480, 0), (640, 80), colors[3], -1)

    cv2.putText(
        frame,
        "RED",
        (40, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "GREEN",
        (180, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "BLUE",
        (340, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "CLEAR",
        (500, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "5 Fingers = SAVE",
        (10, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Thumb+Index = UNDO",
        (300, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )

    cv2.imshow(
        "🔥 ULTRA PRO AIR CANVAS",
        frame
    )

    # X button close
    if cv2.getWindowProperty(
        "🔥 ULTRA PRO AIR CANVAS",
        cv2.WND_PROP_VISIBLE
    ) < 1:
        break

    # ESC OR Q EXIT
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q') or key == 27:
        break

# ---------------- CLEAN EXIT ----------------
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)