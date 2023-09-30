# simpleapp/forms.py
from django import forms
from .models import Name


class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = ['name_text']