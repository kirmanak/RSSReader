# Generated by Django 2.2.7 on 2019-12-02 18:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('reader', '0004_feed_last_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='last_update',
        ),
    ]