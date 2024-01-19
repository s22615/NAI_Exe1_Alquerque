import cv2
import mediapipe as mp
import musicplayer as music
import time
import keyboard

"""
Author
    Sebastian Mackiewicz - PJAIT student

Build hand gesture detection program that will recognize currently displayed gesture. Additionally you can control with
gestures music player by holding ctrl on keyboard.

Before running program install
pip install opencv-python
pip install mediapipe

Make sure you have installed python at least in version 3.10

Music used:
Lofi Study - Music by FASSounds from Pixabay
Good Night - Music by FASSounds from Pixabay
Spirit Blossom - Music by Roman Belov from Pixabay
"""
cooldown_duration = 2
gesture_cooldown_time = 0

def music_controler():
    """Description of the music_controler function
         Controls music by detected gesture
    """
    global gesture_cooldown_time

    if current_time - gesture_cooldown_time >= cooldown_duration:
        #Hi-Five
        if index_finger_tip < middle_y and middle_finger_tip < middle_y and ring_finger_tip < middle_y and pinky_finger_tip < middle_y:
            music_player.pause_song()
            gesture_cooldown_time = current_time
        # Thumbs up
        elif thumb_tip < index_finger_tip and thumb_tip < middle_finger_tip and thumb_tip < ring_finger_tip and thumb_tip < pinky_finger_tip and index_finger_tip < middle_finger_tip and middle_finger_tip < ring_finger_tip and ring_finger_tip < pinky_finger_tip:
            music_player.increase_volume()
            gesture_cooldown_time = current_time
        # Thumbs down
        elif thumb_tip > index_finger_tip and thumb_tip > middle_finger_tip and thumb_tip > ring_finger_tip and thumb_tip > pinky_finger_tip and index_finger_tip > middle_finger_tip and middle_finger_tip > ring_finger_tip and ring_finger_tip > pinky_finger_tip:
            music_player.decrease_volume()
            gesture_cooldown_time = current_time
        # Pointer
        elif index_finger_tip < middle_y and middle_y < middle_finger_tip and middle_y < ring_finger_tip and middle_y < pinky_finger_tip:
            music_player.play_next_song()
            gesture_cooldown_time = current_time
        # Rock & roll
        elif index_finger_tip < middle_y and pinky_finger_tip < middle_y and middle_finger_tip > middle_y:
            music_player.play_song()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
music_player = music.MusicPlayer()

while cap.isOpened():
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            middle_x = sum([landmark.x for landmark in hand_landmarks.landmark]) / len(hand_landmarks.landmark)
            middle_y = sum([landmark.y for landmark in hand_landmarks.landmark]) / len(hand_landmarks.landmark)

            cv2.circle(frame, (int(middle_x * frame.shape[1]), int(middle_y * frame.shape[0])), 10, (0, 255, 0), -1)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
            pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

            gesture = ''
            current_time = time.time()
            ctrl_key_pressed = keyboard.is_pressed('ctrl')

            if ctrl_key_pressed:
                music_controler()

            if index_finger_tip < middle_y and middle_finger_tip < middle_y and ring_finger_tip < middle_y and pinky_finger_tip < middle_y:
                gesture = "Hi-Five"
            elif thumb_tip < index_finger_tip and thumb_tip < middle_finger_tip and thumb_tip < ring_finger_tip and thumb_tip < pinky_finger_tip and index_finger_tip < middle_finger_tip and middle_finger_tip < ring_finger_tip and ring_finger_tip < pinky_finger_tip:
                gesture = 'Thumbs up'
            elif thumb_tip > index_finger_tip and thumb_tip > middle_finger_tip and thumb_tip > ring_finger_tip and thumb_tip > pinky_finger_tip and index_finger_tip > middle_finger_tip and middle_finger_tip > ring_finger_tip and ring_finger_tip > pinky_finger_tip:
                gesture = 'Thumbs down'
            elif index_finger_tip < middle_y and middle_y < middle_finger_tip and middle_y < ring_finger_tip and middle_y < pinky_finger_tip:
                gesture = 'Pointer'
            elif index_finger_tip < middle_y and pinky_finger_tip < middle_y and middle_finger_tip > middle_y:
                gesture = "Rock & roll"
            else:
                gesture = 'Not detected!'

            cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, f'No hand detected!', (frame.shape[1] - 300, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Hand Gesture Detection', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()