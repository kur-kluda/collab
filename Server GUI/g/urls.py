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
from django.urls import path, include
#from a import views as av
from a import grafiki as g
from a import config as c
from a import bluffer as bl
from a import meklet_tables2 as t2
from a import tutorial101_ciud_sensors as tu
from a import tutorial101_crud_hubs as ch
from a import tutorial101_clud_measure as cl

urlpatterns = [
    path('', g.render_templ_grafs, name='dbGplotApp'),
    path('bl', bl.render_bluff, name='bluffApp'),
    path('t', t2.sensor_list, name='t2App'),
    path('t/', t2.FilteredPersonListView.as_view(), name='t2App'),
    path('s', include("a.urls")),
    path('ad', c.config, name='configApp'),
    path('g/', g.render_templ_grafs, name='dbGplotApp'),
    #path('3/', av.dbplot, name='dbplotApp'),
    #path('4/', av.dbplot_date, name='dbplotApp'),
    path('4/', g.render_templ_grafs, name='dbGplotApp'),
    path('admin/', admin.site.urls),
    #path('1/a.txt', redirect(to="/static/e.txt"))
    #path('t/<str:file_name>/', av.view_text, name='viewText'),
    #originally was AIUD (Addnew/Index/Update||Edit/Delete)
#Sensor CIUD
    path('ciud/', tu.index, name='ciud_index'),  
    path('ciud/create/',tu.create, name='ciud_create'),     
    path('ciud/update/<int:nr>/', tu.update, name='ciud_update'), 
    path('ciud/delete/<int:nr>', tu.destroy, name='ciud_destroy'),
# hub CRUD
    path('crud/', ch.index, name='crud_hub_index'),  
    path('crud/create/',ch.create, name='crud_hub_create'),      
    path('crud/update/<int:nr>/', ch.update, name='crud_hub_update'), 
    path('crud/delete/<int:nr>', ch.destroy, name='crud_hub_destroy'),   
# hub CLUD ([kļūd])
    path('clud/', cl.index, name='clud_index'),  
    path('clud/create/',cl.create, name='clud_create'),      
    path('clud/update/<int:nr>/', cl.update, name='clud_update'), 
    path('clud/delete/<int:nr>', cl.destroy, name='clud_destroy'), 
]