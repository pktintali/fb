# Generated by Django 4.0.2 on 2023-04-18 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_user_coins'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reward',
            options={'verbose_name': 'Coupon', 'verbose_name_plural': 'Coupons'},
        ),
        migrations.AlterField(
            model_name='user',
            name='premium_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='premium_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='redeemedPremium',
            field=models.BooleanField(default=False, verbose_name='Redeemed'),
        ),
        migrations.AlterField(
            model_name='user',
            name='shared_fact_counts',
            field=models.IntegerField(default=0, verbose_name='Shared'),
        ),
    ]