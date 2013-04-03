from . import models
from django import forms


class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = (
            'name', 'company_name', 'email', 'phone', 'url', 'goals',
            'deadline', 'message')
