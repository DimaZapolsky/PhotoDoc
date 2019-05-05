from . import db, app
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String)
    photos = db.relationship('Photo', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '' % self.username


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    filename = db.Column(db.Text)
    path = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_wo_bg_path = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    cropped_photo_path = db.Column(db.Text)


db.create_all()
