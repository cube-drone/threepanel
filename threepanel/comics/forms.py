from django import forms

from datetimewidget.widgets import DateTimeWidget

from .models import Comic, Blog


class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        exclude = ['hidden', 'order', 'id', 'slug', 'created', 'updated']
        widgets = {
            'posted': DateTimeWidget(attrs={},
                                     usel10n=True,
                                     bootstrap_version=3)
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ['hidden', 'markdown_rendered', 'slug']
