import os

from flask import Flask, render_template, request

import models
from models import db

app = Flask(__name__)
app.static_folder = "/Users/jaeheon/Desktop/Dev/uzu/static"

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
        return "성공"
    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000", debug=True)
