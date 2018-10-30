# Generated by Django 2.1.1 on 2018-10-30 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_requestpayment_payment_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestpayment',
            name='payment_by',
            field=models.CharField(choices=[('bkash', 'Bkash'), ('rocket', 'Rocket'), ('cash', 'Cash')], default=None, max_length=120),
        ),
    ]