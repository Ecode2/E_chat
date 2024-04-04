from flask import Flask, render_template, send_from_directory
import os, logging
from pathlib import Path
from dotenv import load_dotenv

UPLOAD_FOLDER = Path(__file__).parent/"static/Files"
os.environ["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

# Initialising logger object
hdlr = logging.StreamHandler()
hdlr.formatter = logging.Formatter("%(filename)s :: %(funcName)s :: %(levelname)s -> %(message)s")

logger = logging.Logger("FLASKER_logger")
logger.addHandler(hdlr)

def create_app(config_filename= None):
    
    app = Flask(__name__)
    logger.info(f"Server object created")

    # Load environment variables
    load_dotenv()

    logger.info(f"Loading environment variables ...")

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024
    

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
    
    @app.route("/files/<filename>")
    def all_files(filename: str):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename.split("Files")[0] )

    # Initialise database
    from .model.db import db
    with app.app_context():
        logger.info(f"initializing Database object ...")
        db.init_app(app=app)
        db.create_all()

    # Import blueprints 
    #from .events import sio
    from .views.admin.admin import admin
    from .views.auth.auth import auth, login_manager
    from .views.frontend.home import home
    from .views.frontend.chat import chat
    from E_chat.events import sio

    logger.info(f"initializing Blueprints ...")
    # Initialise blueprints
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(chat)

    # Initialise Login Manager
    login_manager.init_app(app)

    # Initialise socketio
    sio.init_app(app, max_http_buffer_size=50*1024*1024)
    
    return app
