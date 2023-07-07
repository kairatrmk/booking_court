# Generated by Django 4.2.2 on 2023-07-05 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('field_app', '0010_alter_field_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos/')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='field_app.field')),
            ],
        ),
    ]
