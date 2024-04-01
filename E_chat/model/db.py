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
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    room_id = db.Column(db.Integer, db.ForeignKey("chatroom.id"))

    def __repr__(self) -> str:
        return f"<Chat {self.body}>"
    
    @classmethod
    def create(cls, db, author_id: int, room_id: int, body: str):

        if not author_id or not room_id or not body:
            return False

        add_chat = cls(author_id=author_id, room_id=room_id, body=body)
        db.session.add(add_chat)
        db.session.commit()

        return add_chat

    
class Chatroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(50), unique=True)
    roompass = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    room = db.relationship("Chat", backref="chatroom", lazy=True)

    def __repr__(self) -> str:
        return f"<Chatroom {self.roomname}>"