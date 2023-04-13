import re
from paho.mqtt.client import Client
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings
from lampi.models import *
from mixpanel import Mixpanel


MQTT_BROKER_RE_PATTERN = (r'\$sys\/broker\/connection\/'
                          r'(?P<device_id>[0-9a-f]*)_broker/state')

DEVICE_STATE_RE_PATTERN = r'devices\/(?P<device_id>[0-9a-f]*)\/lamp\/changed'


def device_association_topic(device_id):
    return 'devices/{}/lamp/associated'.format(device_id)


class Command(BaseCommand):
    help = 'Long-running Daemon Process to Integrate MQTT Messages with Django'

    def _create_default_user_if_needed(self):
        # make sure the user account exists that holds all new devices
        try:
            User.objects.get(username=settings.DEFAULT_USER)
        except User.DoesNotExist:
            print("Creating user {} to own new LAMPI devices".format(
                settings.DEFAULT_USER))
            new_user = User()
            new_user.username = settings.DEFAULT_USER
            new_user.password = '123456'
            new_user.is_active = False
            new_user.save()

    def _on_connect(self, client, userdata, flags, rc):
        self.client.message_callback_add('$SYS/broker/connection/+/state',
                                         self._monitor_broker_bridges)
        self.client.subscribe('$SYS/broker/connection/+/state')
        self.client.message_callback_add('devices/+/lamp/changed',
                                         self._monitor_lamp_state)
        self.client.subscribe('devices/+/lamp/changed')

    def _create_mqtt_client_and_loop_forever(self):
        self.client = Client()
        self.client.on_connect = self._on_connect
        self.client.connect('localhost', port=50001)
        self.client.loop_forever()

    def _monitor_for_new_devices(self, client, userdata, message):
        print("RECV: '{}' on '{}'".format(message.payload, message.topic))
        # message payload has to treated as type "bytes" in Python 3
        if message.payload == b'1':
            # broker connected
            results = re.search(MQTT_BROKER_RE_PATTERN, message.topic.lower())
            device_id = results.group('device_id')
            try:
                device = Lampi.objects.get(device_id=device_id)
                print("Found {}".format(device))
            except Lampi.DoesNotExist:
                # this is a new device - create new record for it
                new_device = Lampi(device_id=device_id)
                uname = settings.DEFAULT_USER
                new_device.user = User.objects.get(username=uname)
                new_device.save()
                print("Created {}".format(new_device))
                # send association MQTT message
                new_device.publish_unassociated_msg()
                # record a new activation
                self.mp.track(new_device.user.username,
                              "LAMPI Activation", {
                                                   'event_type': 'activations',
                                                   'interface': 'mqtt',
                                                   'device_id': device_id
                                                  }
                              )

    def _monitor_broker_bridges(self, client, userdata, message):
        self._monitor_for_new_devices(client, userdata, message)
        self._monitor_for_connection_events(client, userdata, message)

    def _monitor_for_connection_events(self, client, userdata, message):
        results = re.search(MQTT_BROKER_RE_PATTERN, message.topic.lower())
        device_id = results.group('device_id')
        connection_state = 'unknown'
        if message.payload == b'1':
            print("DEVICE {} CONNECTED".format(device_id))
            connection_state = 'Connected'
        else:
            print("DEVICE {} DISCONNECTED".format(device_id))
            connection_state = 'Disconnected'
        self.mp.track('mqttbridge', "LAMPI {}".format(connection_state),
                      {
                            'event_type': 'devicemonitoring',
                            'interface': 'mqtt',
                            'device_id': device_id
                      }
                      )

    def _monitor_lamp_state(self, client, userdata, message):
        results = re.search(DEVICE_STATE_RE_PATTERN, message.topic.lower())
        device_id = results.group('device_id')
        event_props = {'event_type': 'devicestate',
                       'interface': 'mqtt', 'device_id': device_id}
        event_props.update(json.loads(message.payload.decode('utf-8')))

        self.mp.track('mqttbridge', 'LAMPI State Change', event_props)

    def handle(self, *args, **options):
        self.mp = Mixpanel(settings.MIXPANEL_TOKEN)

        self._create_default_user_if_needed()
        self._create_mqtt_client_and_loop_forever()
