# Generated by Django 2.1.2 on 2018-10-31 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabang', '0005_customer_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_domisili',
            field=models.BooleanField(default=False),
        ),
    ]