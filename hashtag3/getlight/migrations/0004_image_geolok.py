# Generated by Django 3.2.8 on 2021-10-09 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getlight', '0003_image_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='geolok',
            field=models.CharField(default=None, max_length=150, null=True, verbose_name='Геолокация'),
        ),
    ]