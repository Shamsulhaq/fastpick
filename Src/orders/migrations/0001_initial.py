# Generated by Django 2.1.1 on 2018-10-08 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=120)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('shipped', 'Shipped'), ('refunded', 'Refunded')], default='created', max_length=120)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=50.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
            ],
        ),
    ]
