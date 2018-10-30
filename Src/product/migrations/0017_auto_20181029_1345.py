# Generated by Django 2.1.1 on 2018-10-29 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0005_auto_20181016_1550'),
        ('product', '0016_auto_20181027_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='author',
            field=models.ManyToManyField(related_name='author', to='author.BookAuthor'),
        ),
        migrations.RemoveField(
            model_name='booklist',
            name='translator',
        ),
        migrations.AddField(
            model_name='booklist',
            name='translator',
            field=models.ManyToManyField(related_name='translator', to='author.BookAuthor'),
        ),
    ]
