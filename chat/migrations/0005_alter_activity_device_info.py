# Generated by Django 4.0.2 on 2022-09-17 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_activity_uid_alter_message_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='device_info',
            field=models.TextField(),
        ),
    ]