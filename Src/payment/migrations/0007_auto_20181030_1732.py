# Generated by Django 2.1.1 on 2018-10-30 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_auto_20181030_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestpayment',
            name='payment_by',
            field=models.CharField(choices=[('bkash', 'Bkash'), ('rocket', 'Rocket'), ('cash', 'Cash')], max_length=120),
        ),
    ]
