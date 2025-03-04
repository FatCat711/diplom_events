# Generated by Django 4.2.7 on 2024-04-05 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_update_time_rec'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirm'), ('canceled', 'Canceled')], default='pending', max_length=12)),
                ('organization', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(max_length=20)),
                ('last_surname', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_form', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
