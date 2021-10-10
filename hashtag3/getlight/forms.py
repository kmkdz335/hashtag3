from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import *


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ('id', 'img', 'geolok')

class ImageCarForm(ModelForm):
    class Meta:
        model = Image
        fields = ('id', 'geolok')
