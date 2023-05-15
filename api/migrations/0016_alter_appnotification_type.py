# Generated by Django 4.0.2 on 2023-05-14 17:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_appnotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appnotification',
            name='type',
            field=models.CharField(choices=[('INFO', 'INFO'), ('INFO_REVERSED', 'INFO_REVERSED'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR'), ('SUCCESS', 'SUCCESS'), ('QUESTION', 'QUESTION'), ('NO_HEADER', 'NO_HEADER')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]