# python 3.8

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "server"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'




def publish(client):
    msg_count =time.ctime()
    while True:
        time.sleep(1)
        msg = f"Online: {msg_count}"
        result = client.publish(topic,msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Connected `{msg}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count= time.ctime()


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.will_set(topic,payload=("offline") ,qos=0,retain=True,)
    #client.will_set(topic,payload=time.strf("msg_count") ,qos=0,retain=True,)

    client.connect(broker, port)
    return client

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
