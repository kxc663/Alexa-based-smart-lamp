from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Lampi
from django.conf import settings
from lampi.forms import AddLampiForm
from mixpanel import Mixpanel


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'lampi/index.html'

    def get_queryset(self):
        results = Lampi.objects.filter(user=self.request.user)
        return results

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context


class DetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'lampi/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['device'] = get_object_or_404(
            Lampi, pk=kwargs['device_id'], user=self.request.user)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context


class AddLampiView(LoginRequiredMixin, generic.FormView):
    template_name = 'lampi/addlampi.html'
    form_class = AddLampiForm
    success_url = '/lampi'

    def get_context_data(self, **kwargs):
        context = super(AddLampiView, self).get_context_data(**kwargs)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context

    def form_valid(self, form):
        device = form.cleaned_data['device']
        device.associate_and_publish_associated_msg(self.request.user)

        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(device.user.username, "LAMPI Activation",
                 {'event_type': 'activations', 'interface': 'web',
                  'device_id': device.device_id})

        return super(AddLampiView, self).form_valid(form)
