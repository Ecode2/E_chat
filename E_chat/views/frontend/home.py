from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_wtf import FlaskForm
from flask_login import current_user, login_required
from E_chat.model.db import Chatroom, db
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, InputRequired
from werkzeug.security import check_password_hash, generate_password_hash


home = Blueprint('home', __name__, url_prefix="/")


class RoomForm(FlaskForm):
    roomname = StringField("Room Name", validators=[InputRequired(), DataRequired()])
    roompass = PasswordField("Room Password", validators=[DataRequired(), Length(min=3)])
    submit = SubmitField("Submit")

class PassForm(FlaskForm):
    roomId = StringField("Room Id", validators=[InputRequired(), DataRequired()])
    roompass = StringField("Room Password", validators=[InputRequired(), DataRequired()])
    submit = SubmitField("Submit")


@home.route('/', methods=["GET", "POST"])
@login_required
def index():
    roomvalidate = 'False'
    usr = ""

    valid = request.args.get(key="roomvalidate", default='False', type=str)
    if valid == 'True':
        print("true")
        roomvalidate = 'True'
        usr = session["rid"]

    form = RoomForm()
    Rpass = PassForm()
    rooms = Chatroom.query.order_by(Chatroom.date_created)
    
    if Rpass.validate_on_submit():
        roomId = Rpass.roomId.data
        roompass = Rpass.roompass.data
        print("done")

        room = Chatroom.query.filter_by(id=roomId).first()
        if not room:
            flash("Room dosen't exists", category="danger")
            return redirect(url_for("home.index"))

        if check_password_hash(room.roompass, roompass):
            session["room_id"] = roomId
            session["room_validate"] = 'True'
            return redirect(url_for("chat.room", room_id=roomId))
        
        else:
            flash("Room Password Not correct", category="danger")
            return redirect(url_for("home.index"))

    #validate form
    if form.validate_on_submit():

        roomname = form.roomname.data
        roompass = form.roompass.data

        room = Chatroom.query.filter_by(roomname=roomname).first()
        if room:
            flash("Room already exists", category="danger")
            return redirect(url_for("home.index"))
        
        room = Chatroom(roomname=roomname, roompass=generate_password_hash(roompass))
        db.session.add(room)
        db.session.commit()
        
        flash("ChatRoom created successfully", category="success")
        return redirect(url_for("home.index"))

    # clear the form
    form.roomname.data = ""
    form.roompass.data = ""

    # clear the session
    session["rid"] = ""
    session["room_id"] = ""
    session["room_validate"] = 'False'

    return render_template("home.html", usr=usr, roomvalidate=roomvalidate, rooms=rooms, Rpass=Rpass, form=form, current_user=current_user)
 
