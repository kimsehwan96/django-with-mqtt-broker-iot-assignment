import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from paho.mqtt import client as mqtt_client #for mqtt

broker = '3.34.87.77'
port = 1883
topic = "2015146007/"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


class TemplateView(generic.TemplateView):
    template_name = 'mainApp/index.html'
    print("hello!")
    recv_data = None
    def connect_mqtt() -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("COnnected to mqtt broker")
            else:
                print("failed")
        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client
    
    def get_sub_data(client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            recv_data = msg.payload.decode()
        client.subscribe(topic)
        client.on_message = on_message
    
    client = connect_mqtt()