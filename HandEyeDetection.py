import cv2
import dlib
import imutils
from scipy.spatial import distance as dist
from imutils import face_utils
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

def calculate_EAR(eye):
    # calculate the vertical distances
    y1 = dist.euclidean(eye[1], eye[5])
    y2 = dist.euclidean(eye[2], eye[4])

    # calculate the horizontal distance
    x1 = dist.euclidean(eye[0], eye[3])

    # calculate the EAR
    EAR = (y1 + y2) / x1
    return EAR

green_color = (0, 255, 0)
blink_thresh = 0.45
succ_frame = 2
count_frame = 0
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1, min_detection_confidence=0.75,
    min_tracking_confidence=0.75, max_num_hands=2)

(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

detector = dlib.get_frontal_face_detector()
landmark_predict = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')


cap = cv2.VideoCapture(0)

while True:
    # Read video frame by frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = imutils.resize(img, width=640)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = detector(imgRGB)
    for face in faces:
        shape = landmark_predict(imgRGB, face)
        shape = face_utils.shape_to_np(shape)

        lefteye = shape[L_start: L_end]
        righteye = shape[R_start:R_end]

        # Calculate the EAR
        left_EAR = calculate_EAR(lefteye)
        right_EAR = calculate_EAR(righteye)

        # Avg of left and right eye EAR
        avg = (left_EAR + right_EAR) / 2
        if avg < blink_thresh:
            count_frame += 1  # incrementing the frame count
        else:
            if count_frame >= succ_frame:
                cv2.putText(img, 'Blink Detected', (30, 30),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 2)
            else:
                count_frame = 0

    # Process the RGB image
    results = hands.process(imgRGB)

    # If hands are present in image(frame)
    if results.multi_hand_landmarks:

        # Both Hands are present in image(frame)
        if len(results.multi_handedness) == 2:
            # Display 'Both Hands' on the image
            cv2.circle(img, (300, 150), 150, green_color, 10)
            cv2.putText(img, 'Both Hands', (250, 50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.9, (0, 255, 0), 2)

        # If any hand present
        else:
            for i in results.multi_handedness:

                # Return whether it is Right or Left Hand
                label = MessageToDict(i)['classification'][0]['label']

                if label == 'Left':
                    # Display 'Left Hand' on
                    # left side of window
                    cv2.putText(img, label + ' Hand',
                                (20, 50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.9, (0, 255, 0), 2)

                if label == 'Right':
                    # Display 'Left Hand'
                    # on left side of window
                    cv2.putText(img, label + ' Hand', (460, 50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.9, (0, 255, 0), 2)

    # Display Video and when 'q'
    # is entered, destroy the window
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()