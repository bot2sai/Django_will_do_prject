from dataclasses import field
from django.forms import ModelForm
from .models import WillDo

class WillDoForm(ModelForm):
    class Meta:
        model = WillDo
        fields = ['title', 'task', 'important' ]
        