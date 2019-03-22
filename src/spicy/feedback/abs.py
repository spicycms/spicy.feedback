from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from spicy import utils
from . import defaults


DynamicBackendFeedback = utils.backend_factory(
    defaults.FEEDBACK_BACKENDS, 'Feedback',
    delegate_methods=('send_report', 'send_to_clients'))


class BaseFeedbackAbstractModel(DynamicBackendFeedback):
    site = models.ForeignKey(
        Site, verbose_name=_('Site'), default=Site.objects.get_current)
    pattern = models.ForeignKey(
        'feedback.FeedbackPattern', blank=True, null=True,
        verbose_name=_('Fedback pattern'))

    processing_status = models.PositiveSmallIntegerField(
        _('Processing status'), max_length=1,
        choices=defaults.STATUS_TYPE_CHOICES, default=defaults.STATUS_DEFAULT)
    name = models.CharField(_('Name'), max_length=50, blank=True, default='')
    email = models.EmailField(
        _('Email'), max_length=255, blank=True, default='')
    phone = models.CharField(
        _('Phone'), max_length=20, blank=True, default='')
    var1 = models.TextField(_('Var 1'), blank=True, null=True)
    var2 = models.TextField(_('Var 2'), blank=True, null=True)
    var3 = models.TextField(_('Var 3'), blank=True, null=True)
    message = models.TextField(
        _('Message'),  max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default='')
    submit_date = models.DateTimeField(_('Submit date'), auto_now_add=True)
    ip_address = models.IPAddressField(_('IP address'), blank=True, null=True)
    company_name = models.CharField(
        _('Company name'), max_length=100, blank=True, default='')
    url = models.URLField(_('Site URL'), blank=True, default='')

    on_site = CurrentSiteManager()
    objects = models.Manager()

    class Meta:
        db_table = 'fb_feedback'
        ordering = ['-submit_date']
        permissions = [('admin_feedback', 'Admin feedback')]
        abstract = True
        verbose_name = _('Feedback')

    @models.permalink
    def get_admin_url(self):
        return 'feedback:admin:edit', [self.id], {}

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return "TODO:URL"

    def __unicode__(self):
        return '%s @ %s' % (self.name, self.submit_date)

BasePattern = utils.backend_factory(defaults.FEEDBACK_BACKENDS, 'Pattern')


#class FeedbackConsumer(models.Model):
#    class Meta:
#        abstract = True
