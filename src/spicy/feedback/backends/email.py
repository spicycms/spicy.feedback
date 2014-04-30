import traceback
from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import models
from django.template import Context, Template
from django.template.defaultfilters import linebreaksbr
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from spicy import utils
from spicy.core.profile import defaults as pf_defaults
from spicy.core.service import api
from spicy.core.simplepages.abs import EditableTemplateModel
from spicy.utils.printing import print_error, print_info, print_text
from . import base
from .. import defaults


class Pattern(base.Pattern, EditableTemplateModel):
    #email_template = models.CharField(
    #    _('Template'), max_length=255,
    #    choices=utils.find_templates(
    #        defaults.PATTERN_TEMPLATES_PATH, abs_path=False))
    managers_emails = models.TextField(
        _('Managers emails'), max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, default=','.join([
            admin_email for admin_name, admin_email in settings.ADMINS]))
    from_email = models.CharField(
        _('From email'), max_length=255, default=settings.DEFAULT_FROM_EMAIL)
    email_subject = models.CharField(
        _('Email subject'), max_length=255, blank=True, default='')
    email_body = models.TextField(
        _('Email body'),  max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, help_text=_('Auto response feedback text'))
    text_signature = models.TextField(
        _('Email signature'),  max_length=defaults.EMAIL_MAX_LENGTH,
        blank=True, help_text=_('Your signature is added to the letter'))

    def get_text_email(self, feedback=None):
        text_context = Context({
            'feedback': feedback, 'pattern': self, 'page': self,
            'page_content_field': 'content', 'text_mode': True})
        body_template = Template(self.email_body)
        text = body_template.render(text_context)
        text += '\n\n' + self.text_signature
        return text

    def get_html_body(self, feedback=None):
        html_body_context = Context({
            'feedback': feedback, 'pattern': self, 'page': self,
            'page_content_field': 'content'})
        return linebreaksbr(
            Template(self.email_body).render(html_body_context))

    def get_html_email(self, feedback=None):
        html_context = Context({
            'body': self.get_html_body(feedback),
            'site': Site.objects.get_current(),
            'feedback': feedback, 'pattern': self, 'page': self,
            'page_content_field': 'content'})
        return self.get_template().render(html_context)

    def get_mail(self, feedback):
        """
        Return mail
        """

        try:
            from_email = self.from_email
        except:
            from_email = settings.DEFAULT_FROM_EMAIL

        if self.auto_signup:
            Profile = utils.get_custom_model_class(
                pf_defaults.CUSTOM_USER_MODEL)
            Profile.objects.create_inactive_user(feedback.email)

        mail = EmailMultiAlternatives(
            self.email_subject, self.get_text_email(feedback), from_email,
            [feedback.email], headers={'format': 'flowed'})

        mail.attach_alternative(
            self.get_html_email(feedback), "text/html")

        if self.has_attachments():
            for attach in self.attachments():
                if not attach.is_deleted:
                    mail.attach_file(attach.get_abs_path())

        return mail

    def attachments(self):
        return api.register['media'][self].get_instances(
            consumer=self, is_public=True)

    def has_attachments(self):
        return bool(api.register['media'][self].get_instances(
            consumer=self, is_public=True).count())

    class Meta:
        abstract = True


def get_admin_form():
    from spicy.core.simplepages.forms import EditableTemplateForm
    from spicy.feedback.models import FeedbackPattern

    class AdminForm(EditableTemplateForm):
        template_name = forms.ChoiceField(
            label=_('Email template'),
            choices=utils.find_templates(
                defaults.PATTERN_TEMPLATES_PATH, rel_path=True))

        class Meta:
            model = FeedbackPattern
            fields = (
                'is_custom', 'template_name', 'content', 'managers_emails',
                'from_email', 'email_subject', 'text_signature',
                'email_body')

    AdminForm.base_fields['content'].label = _('HTML email code')

    return _('Email settings'), AdminForm

form_template = 'spicy.feedback/admin/parts/email_form.html'


class Feedback(base.Feedback):
    email_has_been_sent = models.BooleanField(default=False, editable=False)

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

    def send_to_customers(self):
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

    class Meta:
        abstract = True


# WTF is this?
"""
def save_same(sender, instance, **kwargs):
    Feedback = get_custom_model_class(defaults.CUSTOM_FEEDBACK_MODEL)

    if instance.email_has_been_sent:
        same_feedbacks = Feedback.objects.filter(
            email=instance.email, type=instance.type,
            email_has_been_sent=False)

        if same_feedbacks:
            for feedback in same_feedbacks:
                feedback.email_has_been_sent = True
                feedback.save()
"""
