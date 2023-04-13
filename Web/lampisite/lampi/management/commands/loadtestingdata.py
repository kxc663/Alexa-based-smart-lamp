from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from lampi.models import Lampi
from uuid import uuid4
import sys

MAX_USERS = 10000

# the upper byte indicates a "Locally Administered" MAC Address
DEVICE_ID_BASE = 0x1e0000000000


class Command(BaseCommand):
    help = 'Load Load-Testing Data'

    def handle(self, *args, **options):

        # create the users, devices, and associations
        for i in range(0, MAX_USERS):
            # create user, if needed
            username = 'user_{:0>6d}'.format(i)
            password = username[::-1]  # reverse string
            u, created = User.objects.get_or_create(username=username)
            if not u.check_password(password):
                u.set_password(password)
            u.save()

            # create device, if needed
            device_id = '{0:x}'.format(DEVICE_ID_BASE + i)
            lm, created = Lampi.objects.get_or_create(device_id=device_id,
                                                      user=u)
            if created:
                lm.save()
            # update progress indicator periodically
            if i % 100 == 0:
                sys.stdout.write('\r')
                per = float(i) / float(MAX_USERS)
                sys.stdout.write("[%-20s] %d%%" % ('='*int(20*per),
                                                   int(100*per)))
                sys.stdout.flush()
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write("Complete                      \n")
        sys.stdout.flush()
