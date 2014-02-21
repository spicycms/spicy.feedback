from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

USE_FEEDBACK_CAPTCHA = getattr(settings, 'USE_FEEDBACK_CAPTCHA', False)

EMAIL_MAX_LENGTH = getattr(settings, 'EMAIL_MAX_LENGTH', 3000)
MESSAGES_PER_MINUTE = getattr(settings, 'MESSAGES_PER_MINUTE', 10)

SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT = getattr(
    settings, 'SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT', True)
CREATE_NEW_ACCOUT = getattr(settings, 'CREATE_NEW_ACCOUNT', False)

IS_PROCESSED, NEW_MAIL, FAIL = range(3)
STATUS_TYPE_CHOICES = getattr(settings, 'STATUS_TYPE_CHOICES', (
    (IS_PROCESSED, _('Is Processed')),
    (NEW_MAIL, _('New Mail')),
    (FAIL, _('Fail')),
))
STATUS_DEFAULT = NEW_MAIL

CUSTOM_FEEDBACK_FORM = getattr(
    settings, 'CUSTOM_FEEDBACK_FORM', 'spicy.feedback.forms.FeedbackForm')

PATTERN_TEMPLATES_PATH = getattr(
    settings, 'PATTERN_TEMPLATES_PATH', 'spicy.feedback/patterns')

USE_DEFAULT_FEEDBACK = getattr(settings, 'USE_DEFAULT_FEEDBACK', True)
CUSTOM_FEEDBACK_MODEL = (
    'feedback.Feedback' if USE_DEFAULT_FEEDBACK else
    settings.CUSTOM_FEEDBACK_MODEL)

FEEDBACK_BACKENDS = getattr(
    settings, 'FEEDBACK_BACKENDS', ('spicy.feedback.backends.email',))


FV_INPUT, FV_TEXTAREA, FV_PHONE, FV_RADIO, FV_SELECT, FV_SELECT_MULTI, \
    FV_CHECKBOX = range(7)
FEEDBACK_VAR_CHOICES = (
    (FV_INPUT, _('Text input')), (FV_TEXTAREA, _('Multiline text area')),
    (FV_PHONE, _('Phone input')), (FV_RADIO, _('Radio buttons')),
    (FV_SELECT, _('Select dropdown')),
    (FV_SELECT_MULTI, _('Select dropdown with multiple choices')),
    (FV_CHECKBOX, _('Checkboxes')))

FEEDBACK_VAR_FIELDS = {
    FV_INPUT: (forms.CharField, ), FV_RADIO: (forms.Select, forms.RadioSelect),
    FV_PHONE: (forms.CharField, ), FV_SELECT: (forms.Select, ),
    FV_SELECT_MULTI: (forms.MultipleChoiceField, ),
    FV_CHECKBOX: (forms.MultipleChoiceField, forms.CheckboxSelectMultiple)}
FEEDBACK_VARS_WITH_OPTIONS = [
    fv[0] for fv in FEEDBACK_VAR_CHOICES
    if not fv[0] in (FV_INPUT, FV_RADIO, FV_PHONE)]
