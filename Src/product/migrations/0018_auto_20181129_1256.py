# Generated by Django 2.1.3 on 2018-11-29 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_auto_20181029_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='translator',
            field=models.ManyToManyField(blank=True, related_name='translator', to='author.BookAuthor'),
        ),
    ]