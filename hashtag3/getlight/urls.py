from django.urls import path
from . import views

app_name = 'GetLight'
urlpatterns = [
    path('', views.index, name='index'),
    path('phone/', views.ImageCreateView.as_view(), name='phone'),
    path('test/', views.test, name='test'),
    path('car/', views.ImageCarCreateView.as_view(), name='car'),
    path('test_car/', views.test_car, name='test_car'),
]