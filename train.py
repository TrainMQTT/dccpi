from dcc_rpi_encoder import *
from dcc_locomotive import *
from dcc_controller import *
import paho.mqtt.client as mqtt


coms.clear()


# SETUP MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("dcc/in")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.payload == "stop":
        l1.stop()
    elif msg.payload == "switch":
        l1.reverse()
    elif msg.payload == "faster":
        if l1.speed < 128:
            new_speed = (l1.speed + 8)
            l1.speed = new_speed
        else:
            l1.speed = 128
    elif msg.payload == "slower":
        if l1.speed > 0:
            new_speed = (l1.speed - 8)
            l1.speed = new_speed
        else:
            l1.speed = 0
    elif msg.payload == "waves":
        print "Following are the waves"
        for wave in coms.waves:
            print wave
            print coms.wave_data[wave]
            print "-----------\n"
        print "idle"
        print coms.idle_wave_data
        print "++++++++++\n"
    elif msg.payload == "on":
        coms.turn_on()
    elif msg.payload == "off":
        coms.turn_off()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.0.0.149", 1883, 60)

client.loop_start()


# Do Train stuff

e = DCCRPiEncoder()
controller = DCCController(e)
l1 = DCCLocomotive("DCC10", 10)
controller.register(l1)
l1.speed_steps = 128
l1.speed = 0
l1.reverse()
controller.start()
