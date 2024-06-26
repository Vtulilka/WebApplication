# Generated by Django 3.2.25 on 2024-04-11 09:33

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('TransactionsApp', '0003_auto_20240319_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
