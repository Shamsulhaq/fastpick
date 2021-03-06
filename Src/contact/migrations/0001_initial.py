# Generated by Django 2.1.1 on 2018-10-10 19:50

import contact.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(max_length=15)),
                ('complain_type', models.CharField(choices=[('sd', 'Slow delivery'), ('pcs', 'Poor client service'), ('rs', 'Rude staff'), ('as', 'About service'), ('o', 'Others')], max_length=5)),
                ('massage', models.TextField()),
                ('screenshots', models.ImageField(blank=True, null=True, upload_to=contact.models.complain_image_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(max_length=15)),
                ('massage', models.TextField()),
            ],
        ),
    ]
