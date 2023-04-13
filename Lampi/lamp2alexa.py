import logging
import os
import json

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import paho.mqtt.client as MQTT
import paho.mqtt.subscribe as subscribe
from lamp_common import *
from lamp_service import *

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on', 'high']
STATUSOFF = ['off', 'low']


global c
c = MQTT.Client()
c.enable_logger()
c.connect('localhost', port=1883, keepalive=60)
c.loop_start()


def on_message(c, userdata, msg):
    global received_message
    received_message = msg.payload.decode()
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")


@ask.launch
def launch():
    speech_text = 'Welcome to use LAMPI!'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('lamp_control', mapping={'status': 'status'})
def lamp_control(status, room):
    if status in STATUSON:
        print('on')
        create_new_state(True)
        return statement('turning {} lights'.format(status))
    elif status in STATUSOFF:
        print('off')
        create_new_state(False)
        return statement('turning {} lights'.format(status))
    else:
        return statement('Sorry not possible.')


def create_new_state(isOn):
    on = isOn
    msg = subscribe.simple("lamp/changed", hostname="localhost")
    new_config = json.loads(msg.payload.decode('utf-8'))
    state = {'color': new_config['color'],
         'brightness': new_config['brightness'], 'on': on, 'client': 'alexa_voice'}
    c.publish('lamp/set_config', json.dumps(state).encode('utf-8'),
          qos=1, retain=True)


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
