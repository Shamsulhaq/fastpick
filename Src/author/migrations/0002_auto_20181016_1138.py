# Generated by Django 2.1.1 on 2018-10-16 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookauthor',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
