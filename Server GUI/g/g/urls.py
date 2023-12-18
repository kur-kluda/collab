"""g URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from a import views as av
from a import grafiki as g

urlpatterns = [
    path('g/', g.render_templ_grafs, name='dbGplotApp'),
    path('3/', av.dbplot, name='dbplotApp'),
    path('4/', av.dbplot_date, name='dbplotApp'),
    path('admin/', admin.site.urls),
    #path('1/a.txt', redirect(to="/static/e.txt"))
    path('t/<str:file_name>/', av.view_text, name='viewText'),
]