from django import forms
from apps.utils.form import FormMixin
from .models import News

# ckeditor
from ckeditor.fields import RichTextField


# ckeditor
class ContentFrom(forms.Form, FormMixin):
    content = RichTextField()


class ArticleForm(forms.ModelForm):
    category = forms.IntegerField()

    class Meta:
        model = News
        fields = ['title', 'desc', 'thumbnail']



