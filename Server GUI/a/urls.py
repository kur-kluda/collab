from django.urls import path

from . import grafiki

urlpatterns = [
    path('', grafiki.render_templ_grafs, name='index'),
]