import sys

from bitfield import BitField

from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from spicy.mediacenter.abs import FatMediaConsumerModel
from spicy.core.service import api, models as service_models
from spicy.utils.printing import print_error

from . import defaults


class FeedbackPattern(service_models.CustomAbstractModel, FatMediaConsumerModel):
    title = models.CharField(
        _('Feedback pattern title'), max_length=250)

    auto_response_timeout = models.PositiveSmallIntegerField(
        _('Timeout for auto response'), max_length = 1, default=15)

    managers_emails = models.TextField(
        _('Managers emails'), max_length=defaults.EMAIL_MAX_LENGTH, 
        blank=True, default=','.join(settings.MANAGERS))

    email_template = models.CharField(
        _('Template'), max_length=255,
        default='default.html')

    from_email = models.CharField(
        _('From email'), max_length=255,
        default=settings.DEFAULT_FROM_EMAIL)

    email_subject = models.CharField(
        _('Email subject'), max_length=255, blank=True, default='')
    email_body = models.TextField(
        _('Email body'),  max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default='')
    
    class Meta:
        db_table = 'fb_pattern'
        

class BaseFeedbackAbstractModel(models.Model):
    """An abstract base feedback class 
    """
    # Metadata about the feedback
    site = models.ForeignKey(
        Site, verbose_name=_('Site'), default=Site.objects.get_current)
    
    pattern = models.ForeignKey(FeedbackPattern, blank=True, null=True)

    email_has_been_sent = models.BooleanField(default=False)
    processing_status = models.PositiveSmallIntegerField(
        _('Processing status'),
        max_length = 1,
        choices = defaults.STATUS_TYPE_CHOICES,
        default = defaults.STATUS_DEFAULT)

    name = models.CharField(_('Name'), max_length=50)
    email = models.EmailField(_('Email'), max_length=75)
    phone = models.CharField(
        _('Phone'), max_length=20, blank=True, default='')

    message = models.TextField(
        _('Message'),  max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default='')

    submit_date = models.DateTimeField(
        _('Submit date'), auto_now_add=True)

    ip_address = models.IPAddressField(
        _('IP address'), blank=True, null=True)

    company_name = models.CharField(
        'Company name', max_length=100, blank=True, default='')

    url = models.URLField(_('Site URL'), blank=True, default='')

    on_site = CurrentSiteManager()
    objects = models.Manager()


    class Meta:        
        ordering = ['-submit_date']
        permissions = [('admin_feedback', 'Admin feedback')]
        abstract = True


    @models.permalink
    def get_admin_url(self):
        return 'feedback:admin:edit', [self.id], {}

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return "TODO:URL"
    
    def send_report(self):
        context = {'message': self, 'site': Site.objects.get_current()}

        subject = render_to_string(
            'spicy.feedback/mail/report_email_subject.txt', context).strip()
        body = render_to_string('spicy.feedback/mail/report_email_body.txt', context)

        send_to = settings.PROJECT_ADMINS
        if self.pattern:
            send_to = map(lambda x: x.split(','), self.pattern.managers_emails.split('\n'))

        mail = EmailMessage(
            subject=subject, body=body, from_email=settings.DEFAULT_FROM_EMAIL,
            to=send_to)
            
        try:
            mail.send()
        except Exception, e:
            sys.stdout.write('Error sending email #%s: %s' % (self.id, str(e)))

    def send_using_pattern(self):
        if self.pattern is None:
            print_error('This feedback {} has not response pattern'.format(self.pk))

        mail = EmailMessage(
            subject=self.pattern.email_subject, body=self.pattern.emai_body, 
            from_email=self.pattern.from_email.split(','),
            to=self.email)

        if self.pattern.attachments:
            mail.attach_file(settings.MEDIA_ROOT + '/HiConversion.pdf')

        mail.send()

        try:
            mail.send()
        except Exception, e:
            sys.stdout.write('Error sending email #%s: %s' % (self.id, str(e)))
            
        
        self.email_has_been_sent = True
        self.save()

    def __unicode__(self):
        return '%s @ %s' % (self.name, self.submit_date)



class Feedback(BaseFeedbackAbstractModel):    
    class Meta:
        db_table = 'fb_feedback'
        abstract = False


