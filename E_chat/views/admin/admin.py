import flask_wtf
from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, url_prefix="/admin")


@admin.route('/')
def index():
    return "<h1>Hello World 2<h1>"
 
