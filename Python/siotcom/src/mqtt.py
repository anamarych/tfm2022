#Local imports
from mongo import Mongo
#External imports
import paho.mqtt.client as mqtt

MQTT_HOST = "localhost" # este concentrador funciona como broker
MQTT_PORT = 1883 #puerto default
MQTT_KEEPALIVE = 60
MQTT_QOS = 2 #comprobar que no se cierre la sesion con este QoS
MQTT_TOPIC = ("4405/000FF001/sensores") #formato aula/concentrador/sensores
#topic de todas las motas en este aula y concentrador "4405/000FF001/sensores"

class MQTT():
    def __init__(self, client_id):
        self.mongo: Mongo = mongo #This is only used on mongo subscriber
        self.mqtt_client = mqtt.Client(client_id) #create client
        self.mqtt_client.on_connect = self.on_connect #on_connect callback
        self.mqtt_client.on_message = self.on_message #on_message callback
        self.mqtt_client.on_publish = self.on_publish #on_publish callback
  
    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        print("Connected to Mosquitto")
        
    def on_message(self, client: mqtt.Client, data, msg: mqtt.MQTTMessage):
        self.mongo.save(msg.payload) #binary format?
    
    def on_publish(self, client: mqtt.Client, data, mid):
        print("Published ", mid)

    def publish(self, topic, data):
        self.mqtt_client.publish(topic, data)
    
    def subscribe(self, topic, qos):
        self.mqtt_client.subscribe(topic, qos)

    def run(self):
        self.mqtt_client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
        self.mqtt_client.loop_start()

    def stop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
