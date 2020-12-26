#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SimpleDHT.h>
#include <string.h>

const char* ON = "On";
const char* OFF = "Off";

const char* ssid = "U+Net2469";
const char* password = "1000003757";
const char* mqtt_server = "3.34.87.77";

int pinDHT22 = 14;
SimpleDHT22 dht22(pinDHT22);
float temperature = 0;
float humidity = 0;

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to");
    Serial.println(ssid);
    WiFi.mode(WIFI_STA); // station 모드
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED){
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi Connected");
    Serial.println("IP address :");
    Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
    char msg[length];
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] : ");
    //동작한다
    for(int i = 0; i < length; i++) {
        msg[i] = (char)payload[i];
    }
    Serial.println(msg);
    if (strcmp(msg, ON)==0){
        Serial.println("On message got");
    }
    //
}

//커넥션 끊어 졌을 때 
void reconnect() {
    while (!client.connected()) {
        Serial.print("Attemp MQTT Conn");
        //create random client id
        String clientId = "ESP8266Client-";
        clientId += String(random(0xffff), HEX);

        if (client.connect(clientId.c_str())) {
            Serial.println("conn");
            client.publish("2015146007/conn", "conn sucess");
            client.subscribe("2015146007/inTopic");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            delay(5000);
        }
    }
}

void get_dht22() {
    int err = SimpleDHTErrSuccess;
    if ((err = dht22.read2(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
        Serial.print("Read DHT22 failed, err="); Serial.println(err); delay(2000);
        return;
    }
}

void setup() {
    pinMode(16, OUTPUT);
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.subscribe("2015146007/inTopic");
    client.setCallback(callback);//setCallback 구현 당시에 callback함수의 인자로
    // void callback(char* topic, byte* payload, unsigned int length) 미리 정의가 된 것?
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    unsigned long now = millis();

    if (now - lastMsg > 2000) {
        lastMsg = now;
        ++value;
        get_dht22();
        snprintf(msg, MSG_BUFFER_SIZE, "{ \"temp\" : %2.f, \"humi\" : %.2f }", temperature, humidity, value);
        //Serial.print("publish message: ");
        //Serial.println(msg);
        client.publish("2015146007/DHT22", msg);
    }
}