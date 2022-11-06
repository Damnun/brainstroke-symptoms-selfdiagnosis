from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    age = db.Column(db.String(16))
    sex = db.Column(db.String(16))
    comment = db.Column(db.String(128))
    filename = db.Column(db.String(128))



class Contact(db.Model):
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    title = db.Column(db.String(50))
    question = db.Column(db.String(500))
    answered = db.Column(db.Integer)