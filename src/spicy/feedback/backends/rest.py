from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from . import base
import json
import requests


class Pattern(base.Pattern):
    send_to_api = models.BooleanField(_('Send lead to API'), default=False)
    token = models.CharField(_('Token (get from CRM admin)'), max_length=255, blank=True, null=True)
    url_to_api = models.CharField(_('URL to rest api'), max_length=300, blank=True, null=True)

    def save_in_api(self, request):
        if self.send_to_api and self.url_to_api and self.token:
            full_request = request.POST.copy()
            full_request.update({'full_name': request.POST.get('name','')})
            full_request.update({'email': request.POST.get('email','')})
            full_request.update({'phone': request.POST.get('phone','')})
            full_request.update({'title': request.POST.get('name','')})
            full_request.update({'birthday':''})
            full_request.update({'lead_source': Site.objects.get_current()})
            msg = u'%s\n%s\n%s\n%s' % (request.POST.get('message', ''),
                                      request.POST.get('var1', ''),
                                      request.POST.get('var2', ''),
                                      request.POST.get('var3', ''))
            full_request.update({'description': msg})
            full_request.update({'lead_source': request.META.get('HTTP_HOST')})
            headers = {'Authorization': 'Token %s' % self.token, 'content-type': 'application/json'}
            data = json.dumps(full_request)
            response = requests.post(self.url_to_api, data=data, headers=headers)

            return response

    class Meta:
        abstract = True


class Feedback(base.Pattern):

    class Meta:
        abstract = True

def get_admin_form():
    from spicy.feedback.models import FeedbackPattern
    from django import forms

    class AdminForm(forms.ModelForm):
        class Meta:
            model = FeedbackPattern
            fields = ('token', 'url_to_api', 'send_to_api')

    return _('REST API settings'), AdminForm
