from django.contrib.sites.models import Site
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from nexmomessage import NexmoMessage
from . import base


class Pattern(base.Pattern):
    send_sms = models.BooleanField(_('Send SMS'))
    nexmo_api_key = models.CharField(
        _('Nexmo API Key'), max_length=8, blank=True, default='')
    nexmo_secret_key = models.CharField(
        _('Nexmo Secret Key'), max_length=8, blank=True, default='')
    sms_from_number = models.CharField(
        _('SMS Sender Number'), max_length=15, blank=True, default='')
    sms_report_numbers = models.TextField(
        _('SMS Report Number'), blank=True, default='',
        help_text=_(
            'Enter one or more numbers separated by line breaks. '
            'Example number is 74951234567'))

    class Meta:
        abstract = True


class Feedback(base.Pattern):
    def send_report(self):
        if (
                self.pattern.send_sms and
                self.pattern.nexmo_api_key and
                self.pattern.nexmo_secret_key and
                self.pattern.sms_from_number and
                self.pattern.sms_report_numbers):
            context = {'feedback': self, 'site': Site.objects.get_current()}
            body = render_to_string(
                'spicy.feedback/sms/report.txt', context)
            for number in self.pattern.sms_report_numbers.splitlines():
                if not number.strip():
                    continue
                text = body[:140].encode('utf-8')
                msg = {
                    'reqtype': 'json',
                    'api_key': self.pattern.nexmo_api_key,
                    'api_secret': self.pattern.nexmo_secret_key,
                    'from': self.pattern.sms_from_number,
                    'to': number,
                    'text': text
                }
                sms = NexmoMessage(msg)
                sms.set_text_info(msg['text'])
                sms.send_request()

    class Meta:
        abstract = True


admin_form = (
    _('SMS settings'),
    ('send_sms', 'nexmo_api_key', 'nexmo_secret_key', 'sms_from_number',
     'sms_report_numbers'))
