import json
from captcha.fields import CaptchaField
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django import forms
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView
from spicy.utils.models import get_custom_model_class
from . import defaults, models

Feedback = get_custom_model_class(defaults.CUSTOM_FEEDBACK_MODEL)


class FeedbackForm(forms.ModelForm):
    if defaults.USE_FEEDBACK_CAPTCHA:
        captcha = CaptchaField(label=_('Captcha'))

    # TODO
    # check pattern.use_captcha instead defaults.USE_FEEDBACK_CAPTCHA

    class Meta:
        model = Feedback
        if defaults.USE_FEEDBACK_CAPTCHA:
            fields = (
                'name', 'email', 'phone', 'message', 'url', 'company_name',
                'var1', 'var2', 'var3', 'captcha')
        else:
            fields = (
                'name', 'email', 'phone', 'message', 'url', 'company_name',
                'var1', 'var2', 'var3')


class AjaxExampleForm(CreateView):
    template_name = ''
    form_class = FeedbackForm

    def form_invalid(self, form):
        if self.request.is_ajax():
            to_json_response = dict()
            to_json_response['status'] = 0
            to_json_response['form_errors'] = form.errors

            to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
            to_json_response['new_cptch_image'] = captcha_image_url(
                to_json_response['new_cptch_key'])

            return HttpResponse(
                json.dumps(to_json_response), content_type='application/json')

    def form_valid(self, form):
        form.save()
        if self.request.is_ajax():
            to_json_response = dict()
            to_json_response['status'] = 1

            to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
            to_json_response['new_cptch_image'] = captcha_image_url(
                to_json_response['new_cptch_key'])

            return HttpResponse(
                json.dumps(to_json_response), content_type='application/json')


class EditFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('site', 'pattern', 'email_has_been_sent', 'ip_address')


class PatternForm(forms.ModelForm):
    class Meta:
        model = models.FeedbackPattern
        fields = (
            'title', 'slug', 'auto_response_timeout', 'use_captcha',
            'auto_signup')


class PatternVariable(forms.ModelForm):
    class Meta:
        model = models.PatternVariable
        fields = ('name', 'value',)
