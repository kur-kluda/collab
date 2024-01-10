"""
ASGI (Asynchronous Server Gateway Interface) config for g project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""
#ASGI ir asinhronais ietvars. Strādā pretēji WSGI.
import os 

from django.core.asgi import get_asgi_application # importē funkciju get_asgi_application no bibliotēkas django.core.asgi.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'g.settings') # iestata sistēmas vides mainīgajā (to nodrošina - os.environ) Django iesatīšanas modeli, kas atrodas g projekta python failā "settings", ko Python Django izmanto, lai zinātu, kā darbojas lietjumprogramma. 

application = get_asgi_application() # mainīgo application iestata kā ASGI lietojumprogrammas objektu.
