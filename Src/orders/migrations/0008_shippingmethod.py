# Generated by Django 2.1.1 on 2018-10-16 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20181016_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(blank=True, choices=[('home delivery', 'Home Delivery'), ('office pick', 'Office Pick')], max_length=100, null=True)),
            ],
        ),
    ]
