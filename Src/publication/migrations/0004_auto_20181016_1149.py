# Generated by Django 2.1.1 on 2018-10-16 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0003_auto_20181016_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
