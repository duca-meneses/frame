from django import forms
from django.forms import ModelForm

from .models import InboxMessage


class InboxNewMessageForm(ModelForm):
    class Meta:
        model = InboxMessage
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Add message ...'}
            ),
        }
