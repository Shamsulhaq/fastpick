# Generated by Django 2.1.1 on 2018-10-29 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestpayment',
            name='status',
            field=models.CharField(choices=[('unpaid', 'UnPaid'), ('paid', 'Paid'), ('pending', 'Pending'), ('refunded', 'Refunded')], default='unpaid', max_length=120),
        ),
    ]
