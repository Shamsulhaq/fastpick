# Generated by Django 2.1.1 on 2018-10-16 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20181016_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='translator',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
