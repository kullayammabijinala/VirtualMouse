import cv2
import mediapipe as mp
import pyautogui
import time
import screen_brightness_control as sbc

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
drawing_utils = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

click_delay = 1
last_click = time.time()

def fingers_up(landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(landmarks[4].x < landmarks[3].x)

    # Other fingers
    for id in [8, 12, 16, 20]:
        fingers.append(landmarks[id].y < landmarks[id - 2].y)
    return fingers

try:
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
                landmarks = hand.landmark
                fingers = fingers_up(landmarks)

                index = landmarks[8]
                x = int(index.x * w)
                y = int(index.y * h)
                screen_x = screen_w / w * x
                screen_y = screen_h / h * y

                # Move Mouse
                if fingers == [0, 1, 0, 0, 0]:
                    pyautogui.moveTo(screen_x, screen_y)

                # Single Click
                if fingers == [0, 1, 1, 0, 0] and time.time() - last_click > click_delay:
                    pyautogui.click()
                    last_click = time.time()

                # Double Click
                if fingers == [0, 1, 1, 1, 0] and time.time() - last_click > click_delay:
                    pyautogui.doubleClick()
                    last_click = time.time()

                # Right Click
                if fingers == [1, 1, 0, 0, 0] and time.time() - last_click > click_delay:
                    pyautogui.rightClick()
                    last_click = time.time()

                # Drag and Drop
                if fingers == [0, 1, 1, 1, 1]:
                    pyautogui.mouseDown()
                else:
                    pyautogui.mouseUp()

                # Take Screenshot
                if fingers == [1, 0, 0, 0, 1] and time.time() - last_click > click_delay:
                    pyautogui.screenshot('screenshot.png')
                    print("Screenshot Taken!")
                    last_click = time.time()

                # Copy Gesture (Thumb + Index close together)
                dist = abs(landmarks[4].x - landmarks[8].x)
                if dist < 0.03 and time.time() - last_click > click_delay:
                    pyautogui.hotkey('ctrl', 'c')
                    print("Copy Action!")
                    last_click = time.time()

                # Volume Up
                if fingers == [1, 1, 1, 1, 1] and time.time() - last_click > click_delay:
                    pyautogui.press("volumeup")
                    last_click = time.time()

                # Volume Down
                if fingers == [0, 0, 0, 0, 0] and time.time() - last_click > click_delay:
                    pyautogui.press("volumedown")
                    last_click = time.time()

                # Brightness Up
                if fingers == [1, 0, 0, 0, 0] and time.time() - last_click > click_delay:
                    sbc.set_brightness(min(sbc.get_brightness()[0] + 10, 100))
                    print("Brightness Increased")
                    last_click = time.time()

                # Brightness Down
                if fingers == [0, 0, 0, 0, 1] and time.time() - last_click > click_delay:
                    sbc.set_brightness(max(sbc.get_brightness()[0] - 10, 0))
                    print("Brightness Decreased")
                    last_click = time.time()

        cv2.imshow("Virtual Mouse", frame)
        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    print("User stopped the program manually.")

finally:
    cap.release()
    cv2.destroyAllWindows()
