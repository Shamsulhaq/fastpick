# Generated by Django 2.1.1 on 2018-10-28 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0010_rent_receive_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rent',
            options={'ordering': ['-return_date']},
        ),
    ]
