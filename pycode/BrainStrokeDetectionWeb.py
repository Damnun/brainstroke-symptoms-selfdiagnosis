# Hand, Eye 인식 + flask web
from flask import Flask, render_template, Response
import cv2
import dlib
import imutils
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
from imutils import face_utils
from scipy.spatial import distance as dist
from soundplay import play
import threading


def calculate_EAR(eye):
    y1 = dist.euclidean(eye[1], eye[5])
    y2 = dist.euclidean(eye[2], eye[4])
    x1 = dist.euclidean(eye[0], eye[3])
    EAR = (y1 + y2) / x1
    return EAR


# Flask settings
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('face-recognition-noused.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    # variable values
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
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = 30
    out = cv2.VideoWriter('video.avi', fourcc, fps, (int(width), int(height)))

    blink_count = 0
    # mode // 0: hand, 1: eye, 2: number, 3: sentence
    mode = 0
    # proceed // 0: left hand, 1: right hand, 2: both hand, 3: eye, 4: number, 5: sentence
    proceed = 0
    proceedSentence = ["왼손을 들어주세요", "오른손을 들어주세요", "양손을 들어주세요", "눈을 깜빡이세요", "숫자를 큰 소리로 읽어주세요", "문장을 큰 소리로 읽어주세요"]
    t = threading.Thread(target=play, args=(proceed + 2, ))
    t.start()
    left_hand_token, right_hand_token, both_hand_token = 0, 0, 0


    while True:
        # Read video frame by frame
        success, img = cap.read()
        img = cv2.flip(img, 1)
        out.write(img)
        img = imutils.resize(img, width=640)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if mode == 1 and blink_count < 100:
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
                        blink_count += 1
                        print(blink_count)
                        cv2.putText(img, "Blink Detected", (30, 30),
                                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 2)
                        if blink_count >= 100:
                            t = threading.Thread(target=play, args=(-2, ))
                            t.start()
                            print("pass")
                    else:
                        count_frame = 0

        # Process the RGB image
        results = hands.process(imgRGB)


        # If hands are present in image(frame)
        if results.multi_hand_landmarks and mode == 0:

            # Both Hands are present in image(frame)
            if len(results.multi_handedness) == 2 and proceed == 2:
                both_hand_token += 1
                # Display 'Both Hands' on the image
                cv2.putText(img, 'Both Hands', (250, 50),
                            cv2.FONT_HERSHEY_COMPLEX,
                            0.9, (0, 255, 0), 2)
                if both_hand_token >= 50:
                    proceed += 1
                    mode += 1
                    t = threading.Thread(target=play, args=(proceed + 2,))
                    t.start()

            # If any hand present
            else:
                for i in results.multi_handedness:

                    # Return whether it is Right or Left Hand
                    label = MessageToDict(i)['classification'][0]['label']


                    if label == 'Left' and proceed == 0:
                        left_hand_token += 1
                        cv2.putText(img, label + ' Hand',
                                    (20, 50),
                                    cv2.FONT_HERSHEY_COMPLEX,
                                    0.9, (0, 255, 0), 2)
                        if left_hand_token >= 50:
                            proceed += 1
                            t = threading.Thread(target=play, args=(proceed + 2,))
                            t.start()

                    if label == 'Right' and proceed == 1:
                        right_hand_token += 1
                        cv2.putText(img, label + ' Hand', (460, 50),
                                    cv2.FONT_HERSHEY_COMPLEX,
                                    0.9, (0, 255, 0), 2)
                        if right_hand_token >= 50:
                            proceed += 1
                            t = threading.Thread(target=play, args=(proceed + 2,))
                            t.start()

        # Display Video and when 'q'
        # is entered, destroy the window
        # cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            out.release()
            cap.release()
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            cv2.waitKey(1)
            cv2.waitKey(1)
            cv2.waitKey(1)
            break

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    out.release()
    cv2.destryAllWindows()
    exit(0)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)