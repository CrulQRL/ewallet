# Generated by Django 2.1.2 on 2018-10-28 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabang', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='id',
        ),
        migrations.AlterField(
            model_name='customer',
            name='user_id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
