from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from spicy.mediacenter.abs import FatMediaConsumerModel
from spicy.core.service import api, models as service_models

from spicy.utils.printing import print_error, print_info, print_text
from spicy import utils 

from . import abs, defaults



class FeedbackPattern(
        service_models.CustomAbstractModel, FatMediaConsumerModel):
    title = models.CharField(
        _('Feedback pattern title'), max_length=250)

    use_captcha = models.BooleanField(default=False)
    auto_signup = models.BooleanField(default=True)

    email_template = models.CharField(
        _('Template'), max_length=255,
        choices=utils.find_templates(defaults.PATTERN_TEMPLATES_PATH), 
        default=None)

    auto_response_timeout = models.PositiveSmallIntegerField(
        _('Timeout for auto response'), max_length=1, default=15)

    managers_emails = models.TextField(
        _('Managers emails'), max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default=','.join([
                admin_email for admin_name, admin_email in settings.ADMINS]))
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


class PatternVariables(models.Model):
    """
    Default variables - are all pattern field

    email, name, phone, var1 etc... 
    """
    name = models.CharField(_('Varibale name'), max_length=50, blank=True, default='')
    value = models.TextField(
        _('Value'),  max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default='')

    class Meta:
        db_table = 'fb_variables'


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

    name = models.CharField(_('Name'), max_length=50, blank=True, default='')
    email = models.EmailField(_('Email'), max_length=255, blank=True, default='')
    phone = models.CharField(
        _('Phone'), max_length=20, blank=True, default='')

    var1 = models.CharField(_('Var 1'), max_length=255, blank=True, default='')
    var2 = models.CharField(_('Var 2'), max_length=255, blank=True, default='')
    var3 = models.CharField(_('Var 3'), max_length=255, blank=True, default='')

    #attachment = 

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
        if settings.DEBUG:
            print_info('New feedback {}. Sending report to managers'.format(self.pk))

        context = {'feedback': self, 'site': Site.objects.get_current()}

        subject = render_to_string('spicy.feedback/mail/report_email_subject.txt', context).strip()
        body = render_to_string('spicy.feedback/mail/report_email_body.txt', context)

        send_to = [admin_email for admin_name, admin_email in settings.ADMINS]
        if self.pattern:
            to_emails = []
            for ems in map(lambda x: x.strip().split(','), 
                           self.pattern.managers_emails.split('\n')):
                for email in ems:
                    if email:
                        to_emails.append(email)
            if to_emails:
                send_to = to_emails
        mail = EmailMessage(
            subject=subject, body=body, from_email=self.email or settings.DEFAULT_FROM_EMAIL, to=send_to)
            
        try:
            mail.send()
        except Exception, e:
            print_error('Error sending email to ADMINS feedback.id={0}: {1}'.format(self.id, str(e)))
            print_text(traceback.format_exc())

    def send_using_pattern(self):
        if not self.email:
            print_info('This feedback {} has no email for customer response generation'.format(self.pk))
            return

        if self.pattern is None:
            print_error('This feedback {} has no response pattern'.format(self.pk))
            return

        try:
            from_email = self.pattern.from_email
        except:
            from_email = settings.DEFAULT_FROM_EMAIL


        # check pattern VARIABLES and render them 
        # make email like HTML if html template exists = render body iside HTML templates
        # fix email encoding
        # 
        mail = EmailMessage(
            subject=self.pattern.email_subject, body=self.pattern.email_body, 
            from_email=from_email,
            to=(self.email,))

        attachments = api.register['media'][self.pattern].get_instances(
            consumer=self.pattern, is_public=True)

        if attachments:
            for attach in attachments:       
                if not attach.is_deleted:
                    mail.attach_file(attach.get_abs_path())
        try:
            mail.send()
            self.email_has_been_sent = True
            self.save()
        except Exception, e:
            print_error('Error sending email id={0}: {1}'.format(self.id, str(e)))
            print_text(traceback.format_exc())

    def __unicode__(self):
        return '%s @ %s' % (self.name, self.submit_date)



if defaults.USE_DEFAULT_FEEDBACK:
    class Feedback(abs.BaseFeedbackAbstractModel):
        class Meta(abs.BaseFeedbackAbstractModel.Meta):
            abstract = False

