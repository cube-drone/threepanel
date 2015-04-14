from django import forms

from .models import SiteOptions

class SiteOptionsForm(forms.ModelForm):
    class Meta:
        model = SiteOptions
        exclude = []
