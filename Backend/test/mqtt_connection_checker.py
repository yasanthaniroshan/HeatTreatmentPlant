import paho.mqtt.client as mqtt


def on_connect(mqtt_client:mqtt.Client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client:mqtt.Client, userdata, msg:mqtt.MQTTMessage):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("sample_user)2131",'sample_password')
client.connect(
    host='broker.hivemq.com',
    port=1883,
    keepalive=60
)

client.publish('django/mqtt', payload="Test message")
client.loop_start()

