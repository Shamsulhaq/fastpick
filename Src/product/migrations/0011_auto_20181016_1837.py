# Generated by Django 2.1.1 on 2018-10-16 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20181016_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='order',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9),
        ),
    ]
