import datetime
import flask_login
from flask_login import current_user
from E_chat.model.db import Users, db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, InputRequired
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash


auth = Blueprint('auth', __name__, url_prefix="/auth")

class SignInForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), DataRequired()])
    password = PasswordField("User Password", validators=[InputRequired(), EqualTo("confirm_pass", message='Passwords Don\'t Match'), Length(min=8, message="Password must be at least 8 characters")])
    confirm_pass = PasswordField("Confirm Password")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), DataRequired()])
    password = PasswordField("User Password", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters")])
    submit = SubmitField("Submit")

login_manager = flask_login.LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Login to join the chatroom"
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    # chr(user_id)
    return Users.query.get(int(user_id))


@auth.route('/', methods=["GET", "POST"])
def signup():

    #Skip If Logged in
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    form = SignInForm()

    #validate form
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()
        if user:
            flash("Username is in use", category="danger")
            return render_template("signup.html", form=form, current_user=current_user)
        
        user = Users(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        # clear the form
        form.username.data = ""
        form.password.data = ""
        form.confirm_pass.data = ""
        
        flask_login.login_user(user, remember=True, duration=datetime.timedelta(minutes=1))
        flash("Account created successfully", category="success")
        return redirect(url_for("home.index"))

    if form.username.data is None:
        # clear the form
        form.username.data = ""
        form.password.data = ""
        form.confirm_pass.data = ""

    return render_template("signup.html", form=form, current_user=current_user)

@auth.route("/login", methods=["GET", "POST"])
def login():
    
    #Skip If Logged in
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    form = LoginForm()

    #validate form
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()
        
        if not user:
            flash("User Doesn't Exists", category="danger")
            return render_template("login.html", form=form, current_user=current_user)
        
        if not check_password_hash(user.password, password):
            flash("Password Incorrect", category="warning")
            return render_template("login.html", form=form, current_user=current_user)
        
        # clear the form
        form.username.data = ""
        form.password.data = ""
        
        flash("Logged In Successful", category="success")
        flask_login.login_user(user, remember=True, duration=datetime.timedelta(minutes=1))
        return redirect(url_for("home.index"))

    if form.username.data is None:
        # clear the form
        form.username.data = ""
        form.password.data = ""
    
    return render_template("login.html", form=form, current_user=current_user)
    


@auth.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("auth.login"))