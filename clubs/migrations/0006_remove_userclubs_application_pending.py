# Generated by Django 3.2.5 on 2021-11-26 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0005_club_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userclubs',
            name='application_pending',
        ),
    ]
