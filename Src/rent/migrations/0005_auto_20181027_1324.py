# Generated by Django 2.1.1 on 2018-10-27 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0004_remove_rentcart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
