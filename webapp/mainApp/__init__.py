#socketio 를 활용해서
#django 서버가 socketio까지 뿌리고
#html에서는 socketio recv해서 Dom을 직접 조작해서 보여주자..
#테스트해보자
from time import sleep
from threading import Thread, Lock
from flask import Flask
from flask_socketio import SocketIO, emit
from time import sleep
from flask_cors import CORS
import random

import multiprocessing as mp

async_mode = None #for buffer flushing
app = Flask(__name__) 
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*', port=9999)
thread = None
thread_lock = Lock()
CORS(app)

@app.route("/")
def index():
    return ("Invaild Path")

@socketio.on('request', namespace='/data')
def push_values(msg):
    emit('rtdata', {'data':random.randint(50)})

#데몬 프로세스 하나 생성 -> socketio 서버 런
p = mp.Process(target=socketio.run, args=(app,), kwargs =  {"debug" :True, "port": 9999},
daemon=True)

p.start() #socketio server run.