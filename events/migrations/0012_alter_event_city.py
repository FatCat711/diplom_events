# Generated by Django 4.2.7 on 2024-03-30 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_remove_event_free_remove_event_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
