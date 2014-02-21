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

    def __unicode__(self):
        return self.title


if defaults.USE_DEFAULT_FEEDBACK:
    class Feedback(abs.BaseFeedbackAbstractModel):
        class Meta(abs.BaseFeedbackAbstractModel.Meta):
            abstract = False


class FeedbackPatternProvider(service_models.ProviderModel):
    pattern = models.ForeignKey(
        FeedbackPattern, verbose_name=_('Feedback pattern'))
    title = models.CharField(
        _('Form title'), max_length=255, default=_('Feedback'))
    button_text = models.CharField(
        _('Button text'), max_length=255, default=_('Submit'))
    js_code = models.TextField(
        _('JavaScript code'), help_text=_('Extra code for analytics, etc'),
        blank=True)

    class Meta:
        db_table = 'fb_provider'


class FeedbackPatternProviderVariable(models.Model):
    provider = models.ForeignKey(FeedbackPatternProvider)
    field = models.CharField(_('Field'), max_length=50)
    field_type = models.PositiveSmallIntegerField(
        _('Field type'), choices=defaults.FEEDBACK_VAR_CHOICES)
    title_display = models.CharField(_('Field title'), max_length=100)
    help_text = models.CharField(
        _('Field help text'), max_length=255, blank=True,
        help_text=_('This field can contain optional help text'))
    position = models.PositiveSmallIntegerField(_('Position'))

    class Meta:
        db_table = 'fb_pvar'
        ordering = 'provider', 'position'

    def make_field(self):
        field_name = unicode(self.field)
        field_data = defaults.FEEDBACK_VAR_FIELDS[self.field_type]

        field_class = field_data[0]

        kwargs = {'label': self.title_display}
        if len(field_data) == 2:
            kwargs['widget'] = field_data[1]
        if self.help_text:
            kwargs['help_text'] = self.title
        if self.options and self.field in defaults.FEEDBACK_VARS_WITH_OPTIONS:
            kwargs['choices'] = [
                (key.split('_', 1)[1], value)
                for key, value in sorted(self.options.iteritemes())]
        else:
            kwargs['max_length'] = getattr(
                abs.BaseFeedbackAbstractModel, field_name).max_length
        field = field_class(kwargs)
        return (field_name, field)


class FeedbackVariableOption(models.Model):
    variable = models.ForeignKey(FeedbackPatternProviderVariable)
    position = models.PositiveIntegerField(_('Position'))
    key = models.CharField(_('Key'), max_length=50)
    value = models.CharField(_('Value'), max_length=255)

    class Meta:
        db_table = 'fb_poption'
        ordering = 'variable', 'position'
