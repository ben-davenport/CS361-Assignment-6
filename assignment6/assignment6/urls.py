from django.contrib import admin
from django.urls import path
from assignment6.views import set_data, get_data, get_closest_earthquake_view, get_weather

urlpatterns = [
    path('set-data/', set_data, name='set-data'),
    path('get-data/', get_data, name='get-data'),
    path('get-closest-earthquake/', get_closest_earthquake_view, name='get_closest_earthquake'),
    path('get-weather/', get_weather, name='get-weather')
]
