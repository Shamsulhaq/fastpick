# Generated by Django 2.1.1 on 2018-10-10 16:15

import author.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter Author name', max_length=255)),
                ('image', models.ImageField(blank=True, upload_to=author.models.upload_author_image_path)),
                ('bio', models.TextField()),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
    ]
