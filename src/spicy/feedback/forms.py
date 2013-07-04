from django import forms
from spicy.utils.models import get_custom_model_class

from . import defaults, models

Feedback = get_custom_model_class(defaults.CUSTOM_FEEDBACK_MODEL)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('name', 'email', 'phone', 'message', 'url', 'company_name', 'pattern')


class EditFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('processing_status',)

class PatternForm(forms.ModelForm):
    class Meta:
        model = models.FeedbackPattern
        fields = (
            'title', 'auto_response_timeout', 'managers_emails',
            'email_subject', 'email_body', 'email_template'
            )


class CreatePatternForm(forms.ModelForm):
    class Meta:
        model = models.FeedbackPattern
        fields = (
            'title', 'auto_response_timeout', 'managers_emails',
            'email_subject', 'email_body'
            )
