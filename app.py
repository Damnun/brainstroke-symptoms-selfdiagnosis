# from flask import Flask, render_template, jsonify, request
#
# app = Flask(__name__)
#
# import requests
# from bs4 import BeautifulSoup
#
# articles = []
#
#
# ## HTML을 주는 부분
# @app.route('/')
# def home():
#     return render_template('index.html')
#
#
# @app.route('/memo', methods=['GET'])
# def listing():
#     return jsonify({'all_articles': articles})
#
#
# ## API 역할을 하는 부분
# @app.route('/memo', methods=['POST'])
# def saving():
#     url_receive = request.form['url_give']
#     comment_receive = request.form['comment_give']
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get(url_receive, headers=headers)
#
#     soup = BeautifulSoup(data.text, 'html.parser')
#
#     title = soup.select_one('meta[property="og:title"]')['content']
#     image = soup.select_one('meta[property="og:image"]')['content']
#     desc = soup.select_one('meta[property="og:description"]')['content']
#
#     doc = {
#         'title': title,
#         'image': image,
#         'desc': desc,
#         'url': url_receive,
#         'comment': comment_receive
#     }
#
#     articles.append(doc)
#
#     return jsonify({'msg': '저장이 완료되었습니다!'})
#
#
# if __name__ == '__main__':
#     app.run('0.0.0.0', port=9090, debug=True)

# face_detect_web_video_save.py

from flask import Flask, render_template, Response
import cv2
import numpy as np
import time
import datetime
import sys

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
num = 3
app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'Image Streaming',
        'time': timeString
    }
    return render_template('test-index.html', **templateData)


def gen_frames():
    camera = cv2.VideoCapture(0)
    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = 30
    out = cv2.VideoWriter('video.avi', fourcc, fps, (int(width), int(height)))

    time.sleep(0.2)
    lastTime = time.time() * 1000.0

    while True:
        ret, image = camera.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)
        delt = time.time() * 1000.0 - lastTime
        s = str(int(delt))
        # print (delt," Found {0} faces!".format(len(faces)) )
        lastTime = time.time() * 1000.0
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.circle(image, (int(x + w / 2), int(y + h / 2)), int((w + h) / 3), (255, 255, 255), 3)
        cv2.putText(image, s, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        cv2.putText(image, timeString, (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        # cv2.imshow("Frame", image)
        out.write(image)

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()
    out.realease()
    cv2.destroyAllWindows()


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)