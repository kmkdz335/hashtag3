import time

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from hashtag3 import settings
from .models import *
from .forms import *
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.generic import UpdateView, DeleteView, View, CreateView
from scripts import script


def index(request):
    return render(request, 'index.html')


def api(request):
    geo = request.GET.get('position', None)
    print(geo)
    return JsonResponse(geo, safe=False)


def search(request):
    q = []
    if request.is_ajax():
        q = request.GET.get('q')
    if q:
        return render(request, 'res.html', {'q': q})


def test(request):
    img = list(Image.objects.all())[-1]
    id = img.id
    geo = img.geolok
    img_per = script.main(img_url=f'C:\\Users\ya\Desktop\hashtag3\hashtag3{img.img.url}', img_id=id, geo=geo)
    return redirect("GetLight:phone")


class ImageCreateView(CreateView):
    permission_required = ''
    template_name = 'phone.html'
    model = Image
    form_class = ImageForm
    raise_exception = True
    success_url = reverse_lazy('GetLight:test')

class ImageCarCreateView(CreateView):
    permission_required = ''
    template_name = 'car.html'
    model = Image
    form_class = ImageCarForm
    raise_exception = True
    success_url = reverse_lazy('GetLight:test_car')

def test_car(request):
    img = list(Image.objects.all())[-1]
    id = img.id
    img_per = script.main(img_url=f'C:\\Users\ya\Desktop\hashtag3\hashtag3{img.img.url}', img_id = id)
    return redirect("GetLight:car")
