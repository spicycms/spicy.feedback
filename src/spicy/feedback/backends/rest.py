from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import base


class Pattern(base.Pattern):
    token = models.CharField(_('Token (generated automatically)'), max_length=255, blank=True, null=True)
    url_to_api = models.CharField(_('URL to rest api'), max_length=300, blank=True, null=True)

    class Meta:
        abstract = True


class Feedback(base.Pattern):
    def save_in_api(self, request):
        if self.url_to_api and self.token:
            full_request = request.POST.copy()
            full_request.update({'lead_source': request.META.get('HTTP_HOST')})
            headers = {'Authorization': 'Token %s' % self.token, 'content-type': 'application/json'}
            data = json.dumps(full_request)
            requests.post(self.url_to_api, data=data, headers=headers)

    class Meta:
        abstract = True

def get_admin_form():
    from spicy.feedback.models import FeedbackPattern

    class AdminForm(forms.ModelsForm):
        class Meta:
            model = FeedbackPattern
            fields = ('token', 'url_to_api')

    return _('REST API settings'), AdminForm