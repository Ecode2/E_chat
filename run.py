from E_chat import create_app

app = create_app()

if __name__=='__main__':

    import eventlet
    from eventlet import wsgi

    wsgi.server( eventlet.listen(("0.0.0.0", 8080)), app )
    

    # Run in development
    #from E_chat.events import sio
    #sio.run(app=app, port=8080, use_reloader=True, debug=True)
