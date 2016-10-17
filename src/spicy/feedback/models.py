from django.core.urlresolvers import reverse
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
    token = models.CharField(_('Token (generated automatically)'), max_length=42, blank=True, null=True)
    url_to_api = models.CharField(_('URL to rest api'), max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'fb_pattern'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('feedback:admin:view-pattern', args=[self.pk])


if defaults.USE_DEFAULT_FEEDBACK:
    class Feedback(abs.BaseFeedbackAbstractModel):
        class Meta(abs.BaseFeedbackAbstractModel.Meta):
            abstract = False



