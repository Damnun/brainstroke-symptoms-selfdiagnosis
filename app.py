import os
from flask import Flask, render_template, request, Response, url_for
import cv2
import dlib
import imutils
import mediapipe as mp
import datetime
from google.protobuf.json_format import MessageToDict
from imutils import face_utils
from scipy.spatial import distance as dist
from soundplay import play
import threading
import models
from models import db

app = Flask(__name__)
app.static_folder = "/Users/jaeheon/Desktop/Dev/uzu/static"
faceCascade = "model/shape_predictor_68_face_landmarks.dat"

# SQLAlchemy 설정
# 현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')
# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/single.html')
def single():
    return render_template("single.html")


@app.route('/index.html')
def index_2():
    return render_template('index.html')


@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        title = request.form.get('title')
        question = request.form.get('question')
        answered = 0
        print(name, email, title, question, answered)
        dbdata = models.Contact(username=name, email=email, title=title, question=question, answered=answered)
        db.session.add(dbdata)
        db.session.commit()
        return "성공"
    return redirect('/')


@app.route('/checkout.html', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        return render_template('checkout.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        sex = request.form.get('sex')
        print(name, email, age, sex)
        # db에 저장후 체크리스트로 넘어가기 (정보를 가져가서 나중에 체크리스트 데이터도 insert할 것)
        return render_template(url_for('checkSymptoms'), name=name, email=email, age=age, sex=sex)
    return redirect('/')


@app.route('/result-search.html', methods=['GET', 'POST'])
def resultSearch():
    if request.method == 'GET':
        return render_template('result-search.html')
    else:
        search_name = request.form.get('name')
        search_email = request.form.get('email')
        print(search_name, search_email)
        # 입력 받아서 db 조회 후 결과 페이지로 넝머가기
        return render_template('result-search.html')
    return redirect('/')


@app.route('/check-symptoms.html', methods=['GET', 'POST'])
def checkSymptoms():
    if request.method == 'GET':
        return render_template('check-symptoms.html')
    else:
        # form에서 데이터 받기
        mynametext = request.form.get('mynametext')
        print(mynametext)
        print(request.form.get)
        return render_template('check-symptoms.html')
    return redirect('/')


@app.route('/video_setting')
def videoSetting():
    """Video streaming home page."""
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'Image Streaming',
        'time': timeString
    }
    return render_template('face-recognition.html', **templateData)


@app.route('/video_feed')
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


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000", debug=True)
