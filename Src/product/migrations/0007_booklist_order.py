# Generated by Django 2.1.1 on 2018-10-16 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20181016_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='booklist',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
