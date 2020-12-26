#socketio 를 활용해서
#django 서버가 socketio까지 뿌리고
#html에서는 socketio recv해서 Dom을 직접 조작해서 보여주자..
#테스트해보자
from logging import debug
from time import sleep
from flask import Flask
from flask_socketio import SocketIO, emit
from time import sleep
from flask_cors import CORS
from .ardu import Arduino

# import multiprocessing as mp
# from multiprocessing import Array #for IPC shared memory

from threading import Thread

async_mode = None #for buffer flushing
app = Flask(__name__) 
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*', port=9999)
CORS(app)

shared_list = [0, 0]
print(shared_list)

ard = Arduino(shared_list)
th2 = Thread(target=ard.run, daemon=True)

@app.route("/")
def index():
    return ("Invaild Path")

@socketio.on('request', namespace='/data')
def push_values(msg):
    emit('rtdata', {'data':ard.get_data()})

#데몬 프로세스 하나 생성 -> socketio 서버 런
th1 = Thread(target=socketio.run, args=(app,), kwargs =  {"debug" :False, "port": 9999, "host" : "0.0.0.0"},
daemon=True)


th1.start()
th2.start()


print("__init__ has done")