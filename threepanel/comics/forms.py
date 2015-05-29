from django import forms

from datetimewidget.widgets import DateTimeWidget

from .models import Comic, Blog, Video, Image


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
        exclude = ['hidden', 'markdown_rendered', 'slug', 'created', 'updated']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ['hidden', 'slug', 'created']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['hidden', 'slug', 'created']
