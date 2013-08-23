from django.conf import settings
from django.utils.translation import ugettext_lazy as _

USE_FEEDBACK_CAPTCHA = getattr(settings, 'USE_FEEDBACK_CAPTCHA', True)

EMAIL_MAX_LENGTH = getattr(settings, 'EMAIL_MAX_LENGTH', 3000)
MESSAGES_PER_MINUTE = getattr(settings, 'MESSAGES_PER_MINUTE', 10)

SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT = getattr(settings, 'SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT', True)

IS_PROCESSED, OK, FAIL, BINGO  = range(4)
STATUS_TYPE_CHOICES = getattr(settings, 'STATUS_TYPE_CHOICES', (
    (IS_PROCESSED, _('IS_PROCESSED')),
    (OK, _('Ok')),
    (FAIL, _('Fail')),
    (BINGO, _('Bingo!')),
))
STATUS_DEFAULT = IS_PROCESSED

CUSTOM_FEEDBACK_FORM = getattr(settings, 'CUSTOM_FEEDBACK_FORM', 'spicy.feedback.forms.FeedbackForm')
CUSTOM_FEEDBACK_MODEL = getattr(settings, 'CUSTOM_FEEDBACK_MODEL', 'feedback.Feedback')
