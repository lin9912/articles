from django.db import models
from django.contrib.auth.models import User

# ckeditor
from ckeditor_uploader.fields import RichTextUploadingField



class Category(models.Model):
    name = models.CharField(max_length=100)


class News(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.URLField()
    desc = models.CharField(max_length=200)
    content = RichTextUploadingField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-pub_date']
