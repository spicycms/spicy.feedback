from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from spicy.mediacenter.abs import FatMediaConsumerModel
from spicy.core.service import api, models as service_models
from . import abs, defaults


class FeedbackPattern(
        service_models.CustomAbstractModel, FatMediaConsumerModel):
    title = models.CharField(
        _('Feedback pattern title'), max_length=250)
    auto_response_timeout = models.PositiveSmallIntegerField(
        _('Timeout for auto response'), max_length=1, default=15)
    managers_emails = models.TextField(
        _('Managers emails'), max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default=','.join([
            admin_email for admin_name, admin_email in settings.ADMINS]))
    email_template = models.CharField(
        _('Template'), max_length=255, default='default.html')
    from_email = models.CharField(
        _('From email'), max_length=255, default=settings.DEFAULT_FROM_EMAIL)
    email_subject = models.CharField(
        _('Email subject'), max_length=255, blank=True,
        default=_('Dear customer! You won 1 million smiles =)'))
    email_body = models.TextField(
        _('Email body'),  max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default='Auto response feedback text')

    def has_attachments(self):
        return bool(api.register['media'][self].get_instances(
            consumer=self, is_public=True).count())

    class Meta:
        db_table = 'fb_pattern'


if defaults.USE_DEFAULT_FEEDBACK:
    class Feedback(abs.BaseFeedbackAbstractModel):
        class Meta(abs.BaseFeedbackAbstractModel.Meta):
            abstract = False
