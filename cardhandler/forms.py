from django import forms
from django.forms.fields import JSONField


class SingleCardJSONForm(forms.Form):
    card_data = forms.JSONField()
