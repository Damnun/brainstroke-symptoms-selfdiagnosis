import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

left_count, left_time, right_count, right_time, both_count, both_time = 0, 0, 0, 0, 0, 0
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1, min_detection_confidence=0.75,
    min_tracking_confidence=0.75, max_num_hands=2)

cap = cv2.VideoCapture(0)

while True:
    # Read video frame by frame
    success, img = cap.read()
    img = cv2.flip(img, 1)

    try:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    except:
        result = (left_count + right_count) // 2
        print("hand count :", result)

    # Process the RGB image
    results = hands.process(imgRGB)

    # If hands are present in image(frame)
    if results.multi_hand_landmarks:

        # Both Hands are present in image(frame)
        if len(results.multi_handedness) == 2:
            # Display 'Both Hands' on the image
            cv2.putText(img, 'Both Hands', (250, 50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.9, (0, 255, 0), 2)

        # If any hand present
        else:
            for i in results.multi_handedness:

                # Return whether it is Right or Left Hand
                label = MessageToDict(i)['classification'][0]['label']

                if label == 'Left':
                    left_count += 1
                    # Display 'Left Hand' on
                    # left side of window
                    cv2.putText(img, label + ' Hand',
                                (20, 50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.9, (0, 255, 0), 2)

                if label == 'Right':
                    right_count += 1
                    # Display 'Left Hand'
                    # on left side of window
                    cv2.putText(img, label + ' Hand', (460, 50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.9, (0, 255, 0), 2)

    # Display Video and when 'q'
    # is entered, destroy the window
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        result = (left_count + right_count) // 2
        print("hand count :", result)
        break
