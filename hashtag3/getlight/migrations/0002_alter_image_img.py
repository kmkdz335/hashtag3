# Generated by Django 3.2.8 on 2021-10-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getlight', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.ImageField(upload_to='img/', verbose_name='Изображение'),
        ),
    ]
