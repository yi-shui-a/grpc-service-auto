from flask import Flask, render_template
from flask_socketio import SocketIO, send
from threading import Thread, Event
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
list = [10, 20, 30, 40]


# 定时任务线程
def background_thread():
    while not thread_stop_event.is_set():
        time.sleep(5)  # 每10秒发送一次消息
        #socketio.emit('message', {'data': 'This is a timed message'})
        socketio.emit('message', {'type':'cpu','data': list})
        time.sleep(5)
        socketio.emit('message', {'type':'disk','data': list})
        time.sleep(5)
        socketio.emit('message', {'type':'memory','data': list})
        time.sleep(5)
        socketio.emit('message', {'type':'running','data': list})


# @app.route('/')
# def index():
#     return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# 启动定时任务线程
thread = Thread(target=background_thread)
thread_stop_event = Event()
thread.start()


if __name__ == '__main__':

    try:
        socketio.run(app, debug=True, port=5000)
    finally:
        thread_stop_event.set()