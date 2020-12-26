import random
from paho.mqtt import client as mqtt_client
from .DAO import DataDAO
from datetime import datetime
import json
class Arduino:
    def __init__(self):
        self.broker = '3.34.87.77'
        self.port = 1883
        self.input_topic = "2015146007/DHT22"
        self.client_id = f'python-mqtt-{random.randint(0, 100)}'
        self.client = None
        self.dao = DataDAO()
        self.temp = None
        self.humid = None
        self.shared_list = None 

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client
    
    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            recv = msg.payload.decode()
            jd = json.loads(recv)
            if jd:
                temp = jd.get('temp')
                humid = jd.get('humid')
                self.temp =  temp
                self.humid = humid
                print("this is got : {}".format(jd))
                self.dao.insert_data(temp, humid)
            else:
                print("no data...")

        client.subscribe(self.input_topic)
        client.on_message = on_message

    def run(self, shared_list):
        self.shared_list = shared_list
        self.client = self.connect_mqtt()
        self.subscribe(self.client)
        self.client.loop_start()

    def get_data(self):
        if ( (self.temp == None) & (self.humid == None)):
            self.shared_list = [0, 0]
        else:
            self.shared_list[self.temp, self.humid]