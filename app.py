import os
from flask import Flask, render_template, request, Response, url_for
import cv2
import dlib
import imutils
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
from imutils import face_utils
from scipy.spatial import distance as dist

import models
from pycode.soundplay import play
import threading
from models import db
from models import User
from models import Contact

# TODO : 음성 인식 및 STT 페이지 구현
# TODO : 배포 및 서버 최종 업로드 구현

app = Flask(__name__)
app.static_folder = "/Users/jaeheon/Desktop/Dev/uzu/static"
faceCascade = "model/shape_predictor_68_face_landmarks.dat"

# SQLAlchemy 설정
basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()

name, email, sex, age, comment = "", "", "", "", ""
left_hand, right_hand, both_hand, eyes, voice = False, False, False, False, False


@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/')
def index2():
    return render_template('home.html')


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/index')
# def index_2():
#     return render_template('index.html')


@app.route('/emergency')
def emergency():
    return render_template('emergency.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        title = request.form.get('title')
        question = request.form.get('question')
        dbdata = Contact(username=name, email=email, title=title, question=question, answered=0)
        db.session.add(dbdata)
        db.session.commit()
        return "성공"
    return redirect('/')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/before', methods=['GET', 'POST'])
def before():
    if request.method == 'GET':
        return render_template('before.html')
    else:
        comment = request.form.get('comment')
        print(name, email, age, sex, comment)
        user = User(username=name, email=email, age=age, sex=sex, comment=comment, filename=name+email+'.avi')
        db.session.add(user)
        db.session.commit()
        return render_template('face-recognition.html')
    return redirect('')


@app.route('/search-result', methods=['GET', 'POST'])
def resultSearch():
    if request.method == 'GET':
        return render_template('search-result.html')
    else:
        search_name = request.form.get('name')
        search_email = request.form.get('email')
        print(search_name, search_email)
        # 입력 받아서 db 조회 후 결과 페이지로 넝머가기
        return render_template('search-result.html')
    return redirect('/')


@app.route('/check-symptoms', methods=['GET', 'POST'])
def checkSymptoms():
    global name
    global email
    global age
    global sex
    if request.method == 'GET':
        return render_template('check-symptoms.html')
    else:
        # form에서 데이터 받기
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        sex = request.form.get('sex')
        return render_template('check-symptoms.html', name=name)
    return redirect('/')


@app.route('/read-before')
def readBefore():
    return render_template('read-before.html')

@app.route('/read')
def read():
    import speech_recognition as sr

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("말해보세요!")
        audio = r.listen(source)
        try:
            transcript = r.recognize_google(audio, language="ko-KR")
            print("인식된 음성 : " + transcript)
        except sr.UnknownValueError:
            print("인식된 음성을 이해할 수 없습니다.")
        except sr.RequestError as e:
            print("STT 서비스에 접근할 수 없습니다. {0}".format(e))
    return render_template('read.html', transcript=transcript)


@app.route('/video_setting', methods=['GET', 'POST'])
def videoSetting():
    if request.method == 'GET':
        return render_template('face-recognition.html')
    else:
        return render_template('face-recognition.html')


@app.route('/videoFeed')
def videoFeed():
    return Response(stroke_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')


def calculate_EAR(eye):
    y1 = dist.euclidean(eye[1], eye[5])
    y2 = dist.euclidean(eye[2], eye[4])
    x1 = dist.euclidean(eye[0], eye[3])
    EAR = (y1 + y2) / x1
    return EAR


def stroke_detection():
    # variable values
    global left_hand, right_hand, both_hand, eyes
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
    out = cv2.VideoWriter('./save_videos/' + name + email + '.avi', fourcc, fps, (int(width), int(height)))

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

        if mode == 1 and blink_count < 50:
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
                        if blink_count >= 50:
                            t = threading.Thread(target=play, args=(-2, ))
                            t.start()
                            print("pass")
                            eyes = True
                            cap.release()
                            out.release()
                            cv2.waitKey(1)
                            cv2.waitKey(1)
                            cv2.waitKey(1)
                            cv2.waitKey(1)
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
                    both_hand = True
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
                            left_hand = True
                            proceed += 1
                            t = threading.Thread(target=play, args=(proceed + 2,))
                            t.start()

                    if label == 'Right' and proceed == 1:
                        right_hand_token += 1
                        cv2.putText(img, label + ' Hand', (460, 50),
                                    cv2.FONT_HERSHEY_COMPLEX,
                                    0.9, (0, 255, 0), 2)
                        if right_hand_token >= 50:
                            right_hand = True
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


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000", debug=True, threaded=True)
