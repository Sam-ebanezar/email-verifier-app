from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    role = db.Column(db.String(10), default='user')

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(300))
    stored_filename = db.Column(db.String(300))
    upload_time = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('uploads', lazy=True))
