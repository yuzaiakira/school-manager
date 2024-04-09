from django import forms
from ckeditor.widgets import CKEditorWidget
from blog.models import PostModel


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label="محتوا")

    class Meta:
        model = PostModel
        exclude = ('author',)
