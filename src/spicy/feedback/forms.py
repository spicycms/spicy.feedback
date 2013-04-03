from django import forms

from . import models

class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = (
            'name', 'company_name', 'email', 'phone', 'url', 'goals',
            'deadline', 'message')
