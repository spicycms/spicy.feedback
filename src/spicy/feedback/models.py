from django.conf import settings
from django.db import models
from django.template import Context, Template, loader
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from spicy.mediacenter.abs import FatMediaConsumerModel
from spicy.core.profile.implementation import Profile
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

    def get_mail(self, feedback):
        """
        
        return mail

        """
        var_dict = dict(feedback=feedback, pattern=self)
        for var in PatternVariable.objects.all():
            var_dict[var.name] = var.value

        context = Context(var_dict)
        body_template = Template(self.email_body)
        text = body_template.render(context)
                
        try:
            from_email = self.from_email
        except:
            from_email = settings.DEFAULT_FROM_EMAIL

        if self.auto_signup:
            Profile.objects.create_inactive_user(feedback.email)

        mail = EmailMultiAlternatives(
            self.email_subject, text, from_email, [feedback.email], 
            headers={'format': 'flowed'})

        if self.email_template:
            html_var_dict = dict(body=text, site=Site.objects.get_current())
            html_var_dict.update(var_dict)
            template = loader.get_template(
                defaults.PATTERN_TEMPLATES_PATH + '/' + self.email_template)

            mail.attach_alternative(
                template.render(Context(html_var_dict)), "text/html")
            
        if self.has_attachments():
            for attach in self.attachments:
                if not attach.is_deleted:
                    mail.attach_file(attach.get_abs_path())

        return mail

    def attachments(self):
        return api.register['media'][self.pattern].get_instances(
            consumer=self.pattern, is_public=True)

    def has_attachments(self):
        return bool(api.register['media'][self].get_instances(
            consumer=self, is_public=True).count())

    class Meta:
        db_table = 'fb_pattern'


class PatternVariable(models.Model):
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



if defaults.USE_DEFAULT_FEEDBACK:
    class Feedback(abs.BaseFeedbackAbstractModel):
        class Meta(abs.BaseFeedbackAbstractModel.Meta):
            abstract = False

