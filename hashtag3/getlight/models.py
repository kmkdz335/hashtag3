from django.db import models
from scripts import script

# Create your models here.


class Image(models.Model):
    """
    Изображение
    """
    id = models.AutoField(primary_key=True)
    img = models.ImageField(verbose_name='Изображение', upload_to='img/')
    percent = models.IntegerField(verbose_name='Процент освещенности', default=None, null=True)
    geolok = models.CharField(max_length=150, verbose_name='Геолокация', default=None, null=True)


def func(self, img):
    img_per = script.main(img_url=f'C:\\Users\ya\PycharmProjects\hashtag3\hashtag3\{img.url}')