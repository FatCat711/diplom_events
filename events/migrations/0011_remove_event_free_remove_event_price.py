# Generated by Django 4.2.7 on 2024-03-30 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_eventuserrating_event_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='free',
        ),
        migrations.RemoveField(
            model_name='event',
            name='price',
        ),
    ]
