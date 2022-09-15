# Generated by Django 4.0.2 on 2022-09-14 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=500)),
                ('img', models.ImageField(blank=True, null=True, upload_to='chat_images/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('uid', models.IntegerField()),
            ],
        ),
    ]