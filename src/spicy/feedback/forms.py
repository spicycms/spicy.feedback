from django import forms
from spicy.utils.models import get_custom_model_class
from captcha.fields import CaptchaField
from django.utils.translation import ugettext_lazy as _

from django.views.generic.edit import CreateView
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import HttpResponse
import json

from . import defaults, models

Feedback = get_custom_model_class(defaults.CUSTOM_FEEDBACK_MODEL)


class FeedbackForm(forms.ModelForm):
    if defaults.USE_FEEDBACK_CAPTCHA:
        captcha = CaptchaField(label=_('Captcha'))

    class Meta:
        model = Feedback
        if defaults.USE_FEEDBACK_CAPTCHA:
            fields = (
                'name', 'email', 'phone', 'message', 'url',
                'company_name', 'pattern', 'var1',
                'var2', 'var3', 'captcha')
        else:
            fields = (
                'name', 'email', 'phone', 'message', 'url',
                'company_name', 'pattern', 'var1', 'var2', 'var3')

class AjaxExampleForm(CreateView):
    template_name = ''
    form_class = FeedbackForm

    def form_invalid(self, form):
        if self.request.is_ajax():
            to_json_responce = dict()
            to_json_responce['status'] = 0
            to_json_responce['form_errors'] = form.errors

            to_json_responce['new_cptch_key'] = CaptchaStore.generate_key()
            to_json_responce['new_cptch_image'] =                                                  captcha_image_url(to_json_responce['new_cptch_key'])

            return HttpResponse(json.dumps(to_json_responce), content_type='application/json')

    def form_valid(self, form):
        form.save()
        if self.request.is_ajax():
            to_json_responce = dict()
            to_json_responce['status'] = 1

            to_json_responce['new_cptch_key'] = CaptchaStore.generate_key()
            to_json_responce['new_cptch_image'] =                                                  captcha_image_url(to_json_responce['new_cptch_key'])

            return HttpResponse(json.dumps(to_json_responce), content_type='application/json')


class EditFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('processing_status',)


class PatternForm(forms.ModelForm):
    class Meta:
        model = models.FeedbackPattern
        fields = (
            'title', 'auto_response_timeout', 'managers_emails',
            'email_subject', 'email_body', 'email_template',
            'from_email',
            )


class CreatePatternForm(forms.ModelForm):
    class Meta:
        model = models.FeedbackPattern
        fields = (
            'title', 'auto_response_timeout', 'managers_emails',
            'email_subject', 'email_body', 'from_email'
            )
