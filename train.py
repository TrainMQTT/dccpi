from dcc_rpi_encoder import *
from dcc_locomotive import *
from dcc_controller import *
from TrainMQTT import *
import paho.mqtt.client as mqtt
import time

coms.clear()

#Get TrainMQTT instance
TMQTT = TrainMQTT();

# SETUP MQTT Listeners
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("DCC")

def on_message(client, userdata, msg):
    command = TMQTT.deserialize(msg.payload);
    if not 'type' in command:
	return
    if command['type'] == 'DCCPi':
        if command['action'] == 'reboot':
            controller.stop()
            controller.start()
        if command['action'] == 'start':
            controller.start()
        if command['action'] == 'stop':
            controller.stop()

    if command['type'] == 'Engine':
    	exists = controller.getLocomotive(command['address'])

    	if not exists:
    		loco = DCCLocomotive(command['address'])
    		controller.register(loco)
        else:
            loco = exists

        TMQTT.mapFrom(command).mapTo(loco);

    if command['type'] == 'Power':
        if command['state']:
            coms.turn_on()
        else:
            coms.turn_off()

#Make MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_start()

# Start Controller
e = DCCRPiEncoder()
controller = DCCController(e)
controller.start()

#Keep Script alive
while True:
    time.sleep(1)
