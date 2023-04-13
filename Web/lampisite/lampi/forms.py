from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Lampi


def device_association_topic(device_id):
    return 'devices/{}/lamp/associated'.format(device_id)


class AddLampiForm(forms.Form):
    association_code = forms.CharField(label="Association Code", min_length=6,
                                       max_length=6)

    def clean(self):
        cleaned_data = super(AddLampiForm, self).clean()
        print("received form with code {}".format(
              cleaned_data['association_code']))
        # look up device with start of association_code
        uname = settings.DEFAULT_USER
        parked_user = get_user_model().objects.get(username=uname)
        devices = Lampi.objects.filter(
            user=parked_user,
            association_code__startswith=cleaned_data['association_code'])
        if not devices:
            self.add_error('association_code',
                           ValidationError("Invalid Association Code",
                                           code='invalid'))
        else:
            cleaned_data['device'] = devices[0]
        return cleaned_data
