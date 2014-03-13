from django.conf import settings
from django.utils.translation import ugettext_lazy as _

USE_FEEDBACK_CAPTCHA = getattr(settings, 'USE_FEEDBACK_CAPTCHA', False)

EMAIL_MAX_LENGTH = getattr(settings, 'EMAIL_MAX_LENGTH', 3000)
MESSAGES_PER_MINUTE = getattr(settings, 'MESSAGES_PER_MINUTE', 10)

SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT = getattr(
    settings, 'SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT', True)
CREATE_NEW_ACCOUT = getattr(settings, 'CREATE_NEW_ACCOUNT', False)

IS_PROCESSED, NEW_MAIL, FAIL, SPAM = range(4)
STATUS_TYPE_CHOICES = getattr(settings, 'STATUS_TYPE_CHOICES', (
    (IS_PROCESSED, _('Is Processed')),
    (NEW_MAIL, _('New Mail')),
    (FAIL, _('Fail')),
    (SPAM, _('Spam')),
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
