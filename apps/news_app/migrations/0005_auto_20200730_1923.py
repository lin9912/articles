# Generated by Django 3.0.3 on 2020-07-30 17:23

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_auto_20200729_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
