# Generated by Django 4.2.2 on 2023-06-29 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='price_hour',
            field=models.IntegerField(default=None, verbose_name='Цена за час'),
        ),
    ]
