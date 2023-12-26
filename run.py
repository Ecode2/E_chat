from E_chat import create_app

app = create_app()

if __name__=='__main__':

    from E_chat.events import sio
    sio.run(app=app, port=8000)
