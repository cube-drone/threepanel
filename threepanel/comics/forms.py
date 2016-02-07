from django import forms

from .models import Comic, Blog, Video, Image


class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        exclude = ['hidden', 'order', 'id', 'slug', 'created', 'updated']

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
