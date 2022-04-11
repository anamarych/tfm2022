# TODO: comprobar funcionamiento para publicar informacion
import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_QOS = 2 #comprobar que no se cierre la sesion con este QoS
MQTT_TOPICS = ("lab4405/sensores") #habra que agregar cual regleta si queremos identificar mejor las motas y no solo por id
MQTT_MSG = ""

def __init__(self):
    self.mqtt_client = mqtt.Client()
    self.mqtt_client.on_connect = self.on_connect
    self.mqtt_client.on_message = self.on_message
    
def on_connect(client:mqtt.Client, data, flgs, rc):
    print("Connected to mosquitto")
    for topic in MQTT_TOPICS:
        client.subscribe(topic, MQTT_QOS)
        
def on_message(self, client: mqtt.Client, data, msg: mqtt.MQTTMessage):
    # TODO: lo que vamos a hacer con el mensaje, idealmente enviarlo a mongoDB
    print("mensaje")
    
def run(self):
    self.mqtt_client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    self.mqtt_client.loop_start()

def stop(self):
    self.mqtt_client.loop_stop()
    self.mqtt_client.disconnect()
