import paho.mqtt.client as paho
from paho import mqtt
from secrets import secrets
import time

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.connected = True
        print("Connection successful.")
    else:
        print("Connection failed with code {}".format(rc))

def on_publish(client, userdata, mid, properties=None):
    print("Published message {}.".format(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed to a topic with qos {}".format(granted_qos[0]))

def on_message(client, userdata, msg):
    print("Received new message on topic {t}:\n{m}".format(t=msg.topic, m=msg.payload))

class Communicator(object):
    def __init__(self):
        self.client = paho.Client(client_id="laptop", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = on_connect
        self.client.connected = False

        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(secrets['mqtt_username'], secrets['mqtt_password'])

        self.client.loop_start()
        print("Attempting connection...")
        self.client.connect(secrets['mqtt_server'], 8883)
        while not self.client.connected:
            print("...")
            time.sleep(1)

        # for verbose output:
        self.client.on_subscribe = on_subscribe
        self.client.on_message = on_message
        self.client.on_publish = on_publish

        self.client.loop_stop()

    def get_messages(self):
        self.client.loop_start()
        time.sleep(1)
        self.client.loop_stop()

    def send_message(self, topic, message, retain=True):
        self.client.loop_start()
        self.client.publish(topic, payload=message, qos=1, retain=retain)
        time.sleep(1)
        self.client.loop_stop()

