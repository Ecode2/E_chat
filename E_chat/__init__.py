from flask import Flask, render_template
import os
from dotenv import load_dotenv

def create_app(config_filename= None):
    
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://piwarjam:fYgSWfDihYh-eGKyquUss3G3vkY-VuL9@drona.db.elephantsql.com/piwarjam' #os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    

    if config_filename is not None:
        app.config.from_pyfile(config_filename)
    
    # Invalid url
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # Internal server erroe
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template("500.html"), 500

    # Initialise database
    from .model.db import db
    with app.app_context():
        db.init_app(app=app)
        db.create_all()

    # Import blueprints 
    #from .events import sio
    from .views.admin.admin import admin
    from .views.auth.auth import auth, login_manager
    from .views.frontend.home import home
    from .views.frontend.chat import chat
    from E_chat.events import sio

    # Initialise blueprints
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(chat)

    # Initialise Login Manager
    login_manager.init_app(app)

    # Initialise socketio
    sio.init_app(app)
    
    return app
    
    

if __name__=='__main__':

    from E_chat.events import sio
    app = create_app()
    
    sio.run(app=app)
