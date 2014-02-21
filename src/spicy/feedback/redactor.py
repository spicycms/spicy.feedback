from django.utils.translation import ugettext_lazy as _
from spicy.redactor import plugins
from . import models


class FeedbackPlugin(plugins.BasePlugin):
    """
    Media plugin for including providers by PK.
    """
    name = 'feedback'
    title = _('Feedback form')
    priority = 10

#    def check(self, model, field_name):
#        return issubclass(model, abs.FeedbackConsumer)

    def render(self, provider_id):
        prov = models.FeedbackPatternProvider.objects.get(pk=provider_id)
        return prov.render_inc()
