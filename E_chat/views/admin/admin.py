import os
from dotenv import load_dotenv
from ..frontend.home import RoomForm
from ..auth.auth import SignInForm
from flask import Blueprint, render_template, flash, redirect, url_for, session, request, abort
from flask_wtf import FlaskForm
from flask_login import current_user, login_required
from E_chat.model.db import Chatroom, db, Users
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, InputRequired
from werkzeug.security import check_password_hash, generate_password_hash


admin = Blueprint('admin', __name__, url_prefix="/admin")

load_dotenv()

class DeleteForm(FlaskForm):
    roomid = StringField("Room Id", validators=[InputRequired(), DataRequired()])
    roomname = StringField("Room Name", validators=[InputRequired(), DataRequired()])
    submit = SubmitField("Submit")

class DeleteUser(FlaskForm):
    userid = StringField("User Id", validators=[InputRequired(), DataRequired()])
    username = StringField("Username", validators=[InputRequired(), DataRequired()])
    submit = SubmitField("Submit")


@admin.route('/', methods=["GET", "POST"])
@login_required
def index():

    if int(current_user.id) != 1 and current_user.username != "Admin" and not check_password_hash(current_user.password, os.getenv("ADMIN_PASSWORD")):
        raise abort(403, description="You are not authorised to access this page.")
    
    delete_form = DeleteForm()
    delete_user = DeleteUser()
    create_room = RoomForm()
    create_user = SignInForm()

    # validate forms
    if create_room.validate_on_submit():

        roomname = create_room.roomname.data
        roompass = create_room.roompass.data

        room = Chatroom.query.filter_by(roomname=roomname).first()
        if room:
            flash("Room already exists", category="danger")
            return redirect(url_for("admin.index"))
        
        room = Chatroom(roomname=roomname, roompass=generate_password_hash(roompass))
        db.session.add(room)
        db.session.commit()
        
        flash("ChatRoom created successfully", category="success")
        return redirect(url_for("admin.index"))
    
    if create_user.validate_on_submit():

        username = create_user.username.data
        password = create_user.password.data

        user = Users.query.filter_by(username=username).first()
        if user:
            flash("Username is in use", category="danger")
            return redirect(url_for("admin.index"))
        
        user = Users(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
    
        flash("Account created successfully", category="success")
        return redirect(url_for("admin.index"))
    
    if delete_form.validate_on_submit():
        roomid = delete_form.roomid.data
        roomname = delete_form.roomname.data

        room = Chatroom.query.filter_by(id=roomid).first()
        if not room:
            flash("Room dosen't exists", category="danger")
            return redirect(url_for("admin.index"))

        if room.roomname != roomname:
            flash("Room name Not correct", category="danger")
            return redirect(url_for("admin.index"))
        
        db.session.delete(room)
        db.session.commit()

        flash("Room deleted successfully", category="success")
        return redirect(url_for("admin.index"))


    if delete_user.validate_on_submit():
        userid = delete_user.userid.data
        username = delete_user.username.data

        user = Users.query.filter_by(id=userid).first()
        if not user:
            flash("User dosen't exists", category="danger")
            return redirect(url_for("admin.index"))

        if user.username != username:
            flash("Username Not correct", category="danger")
            return redirect(url_for("admin.index"))
        
        db.session.delete(user)
        db.session.commit()

        flash("User deleted successfully", category="success")
        return redirect(url_for("admin.index"))


    rooms = Chatroom.query.order_by(Chatroom.date_created)
    users = Users.query.order_by(Users.username)

    return render_template("admin.html", delete_form=delete_form, rooms=rooms, users=users, delete_user=delete_user, create_room=create_room, create_user=create_user, current_user=current_user)