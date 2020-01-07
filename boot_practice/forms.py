from django.forms import Form, ModelForm, HiddenInput
from django import forms

class Stocknum(forms.Form):
    text=forms.CharField(
        label="銘柄コード(半角)",
        widget=forms.TextInput,
        required=True,
    )
