# Generated by Django 4.0.2 on 2023-02-06 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_alter_bgimage_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bgimage',
            name='url',
        ),
        migrations.AddField(
            model_name='bgimage',
            name='imgID',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bgimage',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]