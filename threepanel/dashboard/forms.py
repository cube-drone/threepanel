from django import forms

from .models import SiteOptions, TwitterIntegration


class SiteOptionsForm(forms.ModelForm):
    class Meta:
        model = SiteOptions
        exclude = []

class TwitterIntegrationForm(forms.ModelForm):
    class Meta:
        model = TwitterIntegration
        exclude = ['site']
