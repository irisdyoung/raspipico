# code built up from example at https://github.com/hivemq-cloud/paho-mqtt-client-example/blob/master/simple_example.py
# subject to https://www.apache.org/licenses/LICENSE-2.0
from umqtt.simple import MQTTClient
from wifi import wlan_status
from secrets import secrets
import time

mqtt_server = 'broker.hivemq.com'
client_id = secrets['mqtt_username'].decode('utf-8')
topic = secrets['mqtt_main_topic']
user = secrets['mqtt_username']
password = secrets['mqtt_password']
port = 8883
my_topics = ['{t}/{s}'.format(t=topic, s=subtopic) for subtopic in \
             ['perl_status', 'calendar', 'interactive', 'batch']]

def reconnect():
    print('Failed to connect to mqtt broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

class Communicator(object):

    def __init__(self, tryagain=True):
        try:
            self.mqtt_connect()
        except OSError as e:
            reconnect()
            if tryagain:
                self.__init__()
        self.messages = {}
        for topic in my_topics:
            self.subscribe(topic)
        self.last_checked = time.time()
        self.update()

    def subscribe(self, topic, tryagain=True):
        self.client.subscribe(topic)
        time.sleep(1)
        if not topic in self.messages.keys() and tryagain:
            self.subscribe(topic)

    def msg_callback(self, topic, msg):
        topic, msg = topic.decode('utf-8'), msg.decode('utf-8')
        #if topic not in self.messages.keys() or self.messages[topic] != msg:
        self.messages[topic] = msg
        print('New message on topic {t}: {m}'.format(t=topic, m=msg))

    def mqtt_connect(self):
        self.client = MQTTClient(client_id, mqtt_server, keepalive=3600, ssl=True, \
                                 port=port, user=user, password=password)
        self.client.set_callback(self.msg_callback)
        self.client.connect()

    def send_msg(self, topic, msg, qos=1, retain=True):
        self.client.publish(topic, msg, qos=1, retain=True)

    def update(self, force=False):
        delta = time.time() - self.last_checked
        if delta >= 10 or force:
            self.client.check_msg()
            self.last_checked = time.time()


