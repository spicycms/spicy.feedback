from django.conf import settings
from django.utils.translation import ugettext_lazy as _

FEEDBACK_MAX_LENGTH = getattr(settings, 'FEEDBACK_MAX_LENGTH', 3000)

MY_FEEDBACK_LIST_LIMIT = getattr(settings, 'MY_FEEDBACK_LIST_LIMIT', 100)
PUBLIC_FEEDBACK_LIST_LIMT = getattr(settings, 'PUBLIC_FEEDBACK_LIST_LIMT', 25)

ADMIN_FEEDBACK_PER_PAGE = getattr(settings, 'ADMIN_FEEDBACK_PER_PAGE', 150)

FEEDBACK_TECHNICAL, FEEDBACK_ABUSE, FEEDBACK_OTHER, FEEDBACK_CORRECTION = range(4)
FEEDBACK_TYPE_CHOICES = getattr(settings, 'FEEDBACK_TYPE_CHOICES', (
    (FEEDBACK_TECHNICAL, _('Technical')),
    (FEEDBACK_ABUSE, _('Abuse')),
    (FEEDBACK_OTHER, _('Other')),
    (FEEDBACK_CORRECTION, _('Correction')),
))


GOALS_CHOICES = getattr(
    settings, 'GOALS_CHOICES',
    (('REQUEST_QUICK_LAUNCH', _("Launch the project ASAP")),
     ('REQUEST_MAKE_PROFIT', _("Make site profitable")),
     ('REQUEST_OPTIMIZE_EXPENSES',
      _("Utilize key performance indicator (KPI) analysis for your projects "
        " to detect best development strategy with optimal expenses")),
    ('REQUEST_SECURITY',
     _("Protect site from viruses and hackers, obtain 24/7 technical support")),
    ('REQUEST_TEST_INFRASTRUCTURE',
     _("Test site effectiveness and/or IT infrastructure")),
    )
)

GOALS = [choice[0] for choice in GOALS_CHOICES]
