# Generated by Django 4.0.2 on 2023-02-07 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_remove_publicmessage_uid_publicmessage_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='last_open',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
