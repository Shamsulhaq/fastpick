# Generated by Django 2.1.1 on 2018-10-16 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20181016_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='order',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True),
        ),
    ]
