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

STATUSON = ['on', 'On', 'high']
STATUSOFF = ['off', 'Off', 'low']
BRIGHTNESS_INC = ['increase', 'INCREASE', 'Increase', 'more']
BRIGHTNESS_DEC = ['decrease', 'DECREASE', 'Decrease', 'less']
STATUS = ['State', 'state', 'Status', 'status']

global c
c = MQTT.Client()
c.enable_logger()
c.connect('localhost', port=1883, keepalive=60)
c.loop_start()


@ask.launch
def launch():
    speech_text = 'Welcome to use LAMPI!'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('get_status', mapping={'get_status_op': 'get_status_op'})
def get_status(get_status_op, room):
    if get_status_op in STATUS:
        print('increase brightness')
        current_state = get_current_state()
        isOn = 'on' if current_state['on'] else 'off'
        return statement('Your lampi is currently {}, the hue is {}, the saturation is {}, the brightness is {}'
                         .format(isOn, current_state['color']['h'], current_state['color']['s'], current_state['brightness']))
    else:
        return statement('Can not get the status of your lamp')


@ask.intent('lamp_control', mapping={'status': 'status'})
def lamp_control(status, room):
    if status in STATUSON:
        print('on')
        update_onOff_state(True)
        return statement('turning {} lights'.format(status))
    elif status in STATUSOFF:
        print('off')
        update_onOff_state(False)
        return statement('turning {} lights'.format(status))
    else:
        return statement('Sorry not possible.')


@ask.intent('brightness_control', mapping={'brightness_op': 'brightness_op'})
def lamp_control(brightness_op, room):
    if brightness_op in BRIGHTNESS_INC:
        print('increase brightness')
        update_brightness(True)
        return statement('{} brightness'.format(brightness_op))
    elif brightness_op in BRIGHTNESS_DEC:
        print('decrease brightness')
        update_brightness(False)
        return statement('{} brightness'.format(brightness_op))
    else:
        return statement('Sorry not possible.')


def get_current_state():
    msg = subscribe.simple("lamp/changed", hostname="localhost")
    new_config = json.loads(msg.payload.decode('utf-8'))
    return new_config


def update_onOff_state(isOn):
    on = isOn
    new_config = get_current_state()
    state = {'color': new_config['color'],
             'brightness': new_config['brightness'], 'on': on, 'client': 'alexa_voice'}
    c.publish('lamp/set_config', json.dumps(state).encode('utf-8'),
              qos=1, retain=True)


def update_brightness(isIncrease):
    new_config = get_current_state()
    if isIncrease:
        new_brightness = new_config['brightness'] + 0.2
        if new_brightness <= 1.0:
            state = {'color': new_config['color'],
                     'brightness': new_brightness, 'on': new_config['on'], 'client': 'alexa_voice'}
        else:
            state = {'color': new_config['color'],
                     'brightness': 1.0, 'on': new_config['on'], 'client': 'alexa_voice'}
    else:
        new_brightness = new_config['brightness'] - 0.2
        if new_brightness >= 0.0:
            state = {'color': new_config['color'],
                     'brightness': new_brightness, 'on': new_config['on'], 'client': 'alexa_voice'}
        else:
            state = {'color': new_config['color'],
                     'brightness': 0.0, 'on': new_config['on'], 'client': 'alexa_voice'}
    c.publish('lamp/set_config', json.dumps(state).encode('utf-8'),
              qos=1, retain=True)


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
