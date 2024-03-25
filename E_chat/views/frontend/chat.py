from flask import Blueprint, render_template, redirect, url_for, session, flash
from E_chat.events import sio
from E_chat.model.db import db, Chatroom, Chat, Users
from flask_login import current_user, login_required
from E_chat.events import sio
from flask_socketio import join_room, leave_room, emit
from datetime import datetime
import os
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

chat = Blueprint('chat',__name__, url_prefix="/chat")
load_dotenv()

@chat.route('/<int:room_id>', methods=["GET", "POST"])
@login_required
def room(room_id):
    if int(current_user.id) != 1 and current_user.username != os.getenv("ADMIN_USERNAME") and not check_password_hash(current_user.password, os.getenv("ADMIN_PASSWORD")):
        # Confirm if password has been inputed
        try:     
            if session["room_id"] != room_id and session["room_validate"] != 'True':
                flash("Room password required", category="warning")
                session["rid"] = room_id
                
                return redirect(url_for("home.index", roomvalidate='True'))   

        except KeyError:
            flash("Room password required", category="warning")
            session["rid"] = room_id
            return redirect(url_for("home.index", roomvalidate='True'))

    

    room = Chatroom.query.filter_by(id=room_id).first()
    chats = Chat.query.filter_by(room_id=room_id)
    
    

    users = Users.query.all()
    return render_template('room.html', current_user=current_user, room=room, chats=chats, users=users)


@sio.on("join")
@login_required
def on_join(data):
    
    room_id = data["room_id"]
    join_room(room_id)
    emit("message", {"sender": "System", "message": f"{current_user.username} joined the room "}, room=room_id, broadcast=True)
    print("Joined room")


@sio.on("leave")
@login_required
def on_leave(data):

    room_id = data["room_id"]
    leave_room(room_id)
    emit("message", {"sender": "System", "message": f"{current_user.username} left the room "}, room=room_id, broadcast=True)
    print("Left room")

    # reset session values
    session["rid"] = ""
    session["room_id"] = ""
    session["room_validate"] = 'False'


@sio.on("message")
@login_required
def send_message(data):
    room_id = data["room_id"]
    sender = data['sender']
    message = data["message"]

    add_chat = Chat(author_id=current_user.id, room_id=room_id, body=message)
    db.session.add(add_chat)
    db.session.commit()

    emit("message", {"sender": sender, "message": message}, room=room_id, broadcast=True)
    print("sent a message")