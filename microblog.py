from app import app

if __name__ == "__main__":
    #socketio.run(app)
    app.run(port=8080,debug=True,threaded=True)
