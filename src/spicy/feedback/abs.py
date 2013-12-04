import traceback
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from spicy.utils.printing import print_error, print_info, print_text
from . import defaults


class BaseFeedbackAbstractModel(models.Model):
    # Metadata about the feedback
    site = models.ForeignKey(
        Site, verbose_name=_('Site'), default=Site.objects.get_current)
    pattern = models.ForeignKey(
        'feedback.FeedbackPattern', blank=True, null=True)

    email_has_been_sent = models.BooleanField(default=False)
    processing_status = models.PositiveSmallIntegerField(
        _('Processing status'), max_length=1,
        choices=defaults.STATUS_TYPE_CHOICES, default=defaults.STATUS_DEFAULT)
    name = models.CharField(_('Name'), max_length=50, blank=True, default='')
    email = models.EmailField(
        _('Email'), max_length=255, blank=True, default='')
    phone = models.CharField(
        _('Phone'), max_length=20, blank=True, default='')
    var1 = models.CharField(_('Var 1'), max_length=255, blank=True, default='')
    var2 = models.CharField(_('Var 2'), max_length=255, blank=True, default='')
    var3 = models.CharField(_('Var 3'), max_length=255, blank=True, default='')
    message = models.TextField(
        _('Message'),  max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default='')
    submit_date = models.DateTimeField(_('Submit date'), auto_now_add=True)
    ip_address = models.IPAddressField(_('IP address'), blank=True, null=True)
    company_name = models.CharField(
        'Company name', max_length=100, blank=True, default='')
    url = models.URLField(_('Site URL'), blank=True, default='')

    on_site = CurrentSiteManager()
    objects = models.Manager()

    class Meta:
        db_table = 'fb_feedback'
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
        if settings.DEBUG:
            print_info(
                'New feedback {}. Sending report to managers'.format(self.pk))

        context = {'feedback': self, 'site': Site.objects.get_current()}

        subject = render_to_string(
            'spicy.feedback/mail/report_email_subject.txt', context).strip()
        body = render_to_string(
            'spicy.feedback/mail/report_email_body.txt', context)

        send_to = [admin_email for admin_name, admin_email in settings.ADMINS]
        if self.pattern:
            to_emails = []
            for ems in (
                    x.strip().split(',') for x in
                    self.pattern.managers_emails.split('\n')):
                for email in ems:
                    if email:
                        to_emails.append(email)
            if to_emails:
                send_to = to_emails
        mail = EmailMessage(
            subject=subject, body=body,
            from_email=self.email or settings.DEFAULT_FROM_EMAIL, to=send_to)

        try:
            mail.send()
        except Exception, e:
            print_error(
                'Error sending email to ADMINS feedback.id={0}: {1}'.format(
                    self.id, str(e)))
            print_text(traceback.format_exc())

    def send_using_pattern(self):
        if not self.email:
            print_info(
                'This feedback {} has no email for customer response '
                'generation'.format(self.pk))
            return

        if self.pattern is None:
            print_error(
                'This feedback {} has no response pattern'.format(self.pk))
            return
                 
        mail = self.pattern.get_mail(self)

        try:
            mail.send()
            self.email_has_been_sent = True
            self.save()
        except Exception, e:
            print_error(
                'Error sending email id={0}: {1}'.format(self.id, str(e)))
            print_text(traceback.format_exc())

    def __unicode__(self):
        return '%s @ %s' % (self.name, self.submit_date)



