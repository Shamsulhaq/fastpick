# Generated by Django 2.1.1 on 2018-10-16 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_shipping_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_method',
            field=models.CharField(choices=[('home delivery', 'Home Delivery'), ('office pick', 'Office Pick')], default='home delivery', max_length=100),
        ),
    ]
