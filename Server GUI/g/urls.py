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
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
#from a import views as av
from a import grafiki as g
from a import config as c
from a import bluffer as bl
from a import meklet_tables2 as t2
from a import tutorial101_ciud_sensors as tu
from a import tutorial101_crud_hubs as ch
from a import tutorial101_clud_measure as cl
#from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from a import view_auth
# tīmekļa šabloni aprakstiti ---turpininājums komentāriem.
urlpatterns = [
    #re_path(r'^favicon\.ico$',RedirectView.as_view(url='/static/favicon/favicon.ico')),
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
    re_path(r'^accounts/login/$',
        view_auth.Login.as_view(
            #template_name='admin/login.html',
            extra_context={
                'site_header': 'Gaisa kvalitātes sistēma',
            })),
    path("register/", view_auth.UserRegistration.as_view(), name="user_registration"),
    path("login/", view_auth.Login.as_view(
            #template_name='admin/login.html',
            extra_context={
                'site_header': 'Gaisa kvalitātes sistēma',
            }), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout_accs"),
    #path('1/a.txt', redirect(to="/static/e.txt"))
    #path('t/<str:file_name>/', av.view_text, name='viewText'),
    #originally was AIUD (Addnew/Index/Update||Edit/Delete)
#Sensor CIUD
    path('ciud/', tu.index, name='ciud_index'), #Lietotājam piekļūstot URL, kas atbilst paraugam 'ciud/', Django izsauks 'tu.index' skata funkciju, lai apstrādātu pieprasījumu. Pie tam šim URL rakstam ir piešķirts nosaukums 'ciud_index'.
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
    #path('clud/', cl.index, name='clud_index', kwargs={"success": False}), 
    path('clud/create/',cl.create, name='clud_create'),      
    re_path(r'^clud/update/(?P<measurement>[^/]+)/(?P<range_low>[\+-]?\d+\.\d+)/(?P<range_high>[\+-]?\d+\.\d+)/(?P<range_step>[\+]?\d+\.\d+)/$', cl.update, name='clud_update'), #'re_path' ir funkcija Django, kas tiek izmantota, lai definētu URL saiti ar normālām izteiksmēm. 'r'^clud/update/(?P<measurement>[^/]+)/(?P<range_low>[\+-]?\d+\.\d+)/(?P<range_high>[\+-]?\d+\.\d+)/(?P<range_step>[\+]?\d+\.\d+)/$'' Tā ir izteiksme, kurai URL ir jāatbilst. Tātad, pa daļām: '^clud/update/' šī daļa no izteiksmes nodrošina to, ka URL sākas ar 'clud/update'; '(?P<measurement>[^/]+)' šī daļa no izteiksmes nosauc daļu no URL par 'measurement' un tā izmanto izteiksmi '[^/]+', lai tā sakristu ar vienu vai vairākām rakstzīmēm, kas nav '/'; '/(?P<range_low>[\+-]?\d+\.\d+)' šī daļa no izteiksmes nosauc daļu no URL par 'range_low', tas atļauj neobligātu plusa un mīnusa izmantošanu '[\+-]?', vēl var izmantot vienu vai vairākus ciparus '\d+', vēl var izmantot punktu '\.' un vienu vairākus ciparus '\d+'; '/(?P<range_high>[\+-]?\d+\.\d+)' strādā tāpat kā iepriekšējais, vienkārši nosaukts atšķirīgi, tas ir, 'range_high'; '/(?P<range_step>[\+]?\d+\.\d+)/$' šī daļa no izteiksmes nosauc daļu no URL par 'range_step' ar neobligātu plusa zīmi, pie tam cipariem, punktu un vēl cipariem, '$' beigās nodrošina to, ka šablons sakrīt ar URL beigām. 'cl.update' ir skata funkcija, kas tiks izsaukta, kad norādītais URL šablons ir atbilstošs. 'name='člud_update'' ir izteiksme, kas piešķir nosaukumu URL šablonam, kas ir vajadzīgs, lai to izmantotu, kā atsauci citās koda daļās, nosaukums ir iestatīts uz 'clud_update'.
    re_path(r'^clud/delete/(?P<measurement>[^/]+)/(?P<range_low>[\+-]?\d+\.\d+)/(?P<range_high>[\+-]?\d+\.\d+)/(?P<range_step>[\+]?\d+\.\d+)/$', cl.destroy, name='clud_destroy'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #static() ir funkcija Django, lai pasniegtu statiskos failus izstrādes procesā. 'statiskie faili'ietver gan parastos statiskos failus, gan multivides failus. 'settings.MEDIA_URL' ir URL prefikss multivides failu apkalpošanai, tas ir nodefinēts Django projekta iestatījumos. 'document_root=settings.MEDIA_ROOT', kas norāda lokālo failu sistēmas ceļu, kur multivides faili tiek glabāti un 'settings.MEDIA_ROOT' ir viens no iestatījumiem Django projektā, kas glabā pilnīgu failu sistēmas ceļu uz direktoriju, kur multivides faili tiek augšupielādēti.