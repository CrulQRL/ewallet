# Generated by Django 2.1.2 on 2018-10-28 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200)),
                ('nama', models.CharField(max_length=200)),
                ('saldo', models.IntegerField(default=0)),
            ],
        ),
    ]