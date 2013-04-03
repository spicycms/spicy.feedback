import sys

from bitfield import BitField

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from spicy.core.siteskin import defaults as sk_defaults

from . import defaults

class BaseFeedbackAbstractModel(models.Model):
    """
    An abstract base class that any custom feedback models probably should
    subclass.
    """

    # Metadata about the feedback
    site = models.ForeignKey(
        Site, verbose_name=_('Site'), default=Site.objects.get_current)

    on_site = CurrentSiteManager()
    objects = models.Manager()

    class Meta:
        abstract = True

    @models.permalink
    def get_absolute_url(self):
        return 'feedback:admin:message-details', [self.id], {}

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return "TODO:URL"

    def __unicode__(self):
        return '%s @ %s' % (self.name, self.submit_date)


class Message(BaseFeedbackAbstractModel):
    name = models.CharField(_('Sender name'), max_length=50)
    company_name = models.CharField(
        'Company name', max_length=100, blank=True, default='')
    email = models.EmailField(_('Sender email'), max_length=75)
    phone = models.CharField(
        _('Sender phone'), max_length=20, blank=True, default='')
    url = models.URLField(_('Site URL'), blank=True, default='')
    message = models.TextField(
        _('Message'),  max_length=defaults.FEEDBACK_MAX_LENGTH,
        blank=True, default='')
    fb_type = models.PositiveSmallIntegerField(
        _('Feedback type'), max_length=1,
        choices=defaults.FEEDBACK_TYPE_CHOICES, default=defaults.FEEDBACK_OTHER)
    goals = BitField(verbose_name=_('Goals'), flags=defaults.GOALS)
    deadline = models.PositiveSmallIntegerField(_('Deadline'))
    submit_date = models.DateTimeField(
        _('Submit date'), auto_now_add=True)
    ip_address = models.IPAddressField(
        _('IP address'), blank=True, null=True)

    class Meta:
        db_table = 'fb_msg'
        ordering = ['-submit_date']
        permissions = [('view_messages', 'View messages')]

    def get_goals_data(self):
        return {
            'GOALS': [bit.mask for bit in self.__class__.goals.itervalues()],
            'GOALS_DICT': dict(
                (bit.mask, defaults.GOALS_CHOICES[i][1])
                for i, bit in enumerate(self.__class__.goals.itervalues()))
        }

    def send_report(self):
        context = {'message': self, 'site': Site.objects.get_current()}
        context.update(self.get_goals_data())
        subject = render_to_string(
            '%s/feedback/report_email_subject.txt' % sk_defaults.SITESKIN,
            context).strip()
        body = render_to_string(
            '%s/feedback/report_email_body.txt' % sk_defaults.SITESKIN,
            context)

        mail = EmailMessage(
            subject=subject, body=body, from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.PROJECT_ADMINS)

        try:
            mail.send()
        except Exception, e:
            sys.stdout.write('Error sending email #%s: %s' % (self.id, str(e)))
