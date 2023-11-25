from E_chat import create_app
from E_chat.events import sio

app = create_app()

if __name__=='__main__':
    sio.run(app=app, host="0.0.0.0", port=5000)