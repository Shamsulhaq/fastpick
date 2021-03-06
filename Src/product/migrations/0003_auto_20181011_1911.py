# Generated by Django 2.1.1 on 2018-10-11 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20181010_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='descriptions',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='regular_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True),
        ),
    ]
