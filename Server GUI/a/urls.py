from django.urls import path

from . import views

urlpatterns = [
    path('', views.dbplot_date, name='index'),
]