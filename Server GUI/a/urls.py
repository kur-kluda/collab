from django.urls import path, re_path
from . import meklet_sens as s
from . import grafiki

urlpatterns = [
    #path('<str:renderer>/', s.search_sensors),
    re_path(r'(?P<renderer>.*)', s.search_sensors),
]