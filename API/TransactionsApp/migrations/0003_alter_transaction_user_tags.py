# Generated by Django 3.2.25 on 2024-04-22 09:51

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('TransactionsApp', '0002_auto_20240422_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='user_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
