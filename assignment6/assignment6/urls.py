"""
URL configuration for assignment6 project.
Currently:
/set-data with a POST will add data to the database
/get-data with a GET will retrieve the most current data
"""
from django.contrib import admin
from django.urls import path
from assignment6.views import set_data, get_data, get_closest_earthquake_view

urlpatterns = [
    path('set-data/', set_data, name='set-data'),
    path('get-data/', get_data, name='get-data'),
    path('get-closest-earthquake/', get_closest_earthquake_view, name='get_closest_earthquake'),
]
