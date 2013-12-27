from django.db import models
from django.utils.translation import ugettext_lazy as _
from spicy.core.service import models as service_models
from spicy.mediacenter.abs import FatMediaConsumerModel
from . import abs, defaults


class FeedbackPattern(
        service_models.CustomAbstractModel, FatMediaConsumerModel,
        abs.BasePattern):
    title = models.CharField(
        _('Feedback pattern title'), max_length=250)
    slug = models.SlugField(
        _('Slug'), unique=True,
        default=lambda: 'feedback' + str(FeedbackPattern.objects.count() + 1))
    use_captcha = models.BooleanField(default=False)
    auto_signup = models.BooleanField(default=True)
    auto_response_timeout = models.PositiveSmallIntegerField(
        _('Timeout for auto response'), max_length=1, default=15)

    class Meta:
        db_table = 'fb_pattern'


class PatternVariable(models.Model):
    """
    Default variables - are all pattern field

    email, name, phone, var1 etc...
    """
    name = models.CharField(
        _('Varibale name'), max_length=50, blank=True, default='')
    value = models.TextField(
        _('Value'),  max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default='')

    class Meta:
        db_table = 'fb_variables'


if defaults.USE_DEFAULT_FEEDBACK:
    class Feedback(abs.BaseFeedbackAbstractModel):
        class Meta(abs.BaseFeedbackAbstractModel.Meta):
            abstract = False
