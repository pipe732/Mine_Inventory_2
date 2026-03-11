from django.contrib import admin
from django.urls import path
from mine_inventory.views import *

urlpatterns = [
    path('', home, name='home'),
]

