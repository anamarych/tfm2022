# TODO: comprobar funcionamiento para publicar informacion
import paho.mqtt.client as mqtt

MQTT_HOST = "localhost" # este concentrador funciona como broker
MQTT_PORT = 1883 #puerto default
MQTT_KEEPALIVE = 60
MQTT_QOS = 2 #comprobar que no se cierre la sesion con este QoS
MQTT_TOPIC = ("4405/000FF001/sensores") #formato aula/concentrador/sensores
#topic de todas las motas en este aula y concentrador "4405/000FF001/sensores"

def __init__(self):
    self.mqtt_client = mqtt.Client("000FF001") #create client
    self.mqtt_client.on_connect = self.on_connect #on_connect callback
    self.mqtt_client.on_message = self.on_message #on_message callback
  
def on_connect(client:mqtt.Client, data, flags, rc):
    print("Connected to Mosquitto")
    client.subscribe(topic, MQTT_QOS)
        
def on_message(self, client: mqtt.Client, data, msg: mqtt.MQTTMessage):
    # TODO: lo que vamos a hacer con el mensaje, idealmente enviarlo a mongoDB
    print(msg)
    
def run(self):
    self.mqtt_client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
    self.mqtt_client.loop_start()

def stop(self):
    self.mqtt_client.loop_stop()
    self.mqtt_client.disconnect()
