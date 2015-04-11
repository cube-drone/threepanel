from django import forms

from datetimewidget.widgets import DateTimeWidget

from .models import Comic 

class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        exclude = ['hidden']
        widgets = {
            'posted':DateTimeWidget(attrs={},
                                    usel10n=True,
                                    bootstrap_version=3)
        }
