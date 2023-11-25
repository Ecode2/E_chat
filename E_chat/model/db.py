from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)

    chats = db.relationship("Chat", backref="author", lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("chatroom.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Chat {self.body}>"

class Chatroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(50), nullable=False, unique=True)
    roompass = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    room = db.relationship("Chat", backref="chatroom", lazy=True)

    def __repr__(self) -> str:
        return f"<Chatroom {self.roomname}>"