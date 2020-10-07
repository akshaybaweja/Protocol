import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import pyserial
import sys

ser = serial.Serial()
ser.baudrate = 115200
ser.port = sys.argv[1]
ser.open()

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if ser.is_open:
        ser.write(msg.payload)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("mqtt.eclipse.org", 1883, 60)
mqttc.subscribe("esprotocol", 0)

mqttc.loop_forever()