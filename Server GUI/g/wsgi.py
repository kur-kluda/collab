"""
WSGI (Web Server Gateway Interface) config for g project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
#WSGI ir sihronais ietvars, starp tīmekļa serveri un to lietotājprogrammām. Respektīvi, tīmekļa serveris gaida, kamēr lietojumprogramma pabeigs HTTP pieprasījuma apstrādi, jo tiek apstrādāts pa vienam pieprasījumam.
import os # nodrošina miejiedarbību ar operētājsistēmu.
import sys # nodrošina informācijas iegūšanu par Python izpildes sistēmu.
import site # nodrošina, ka tiks pievienotas direktorijas sistēmas ceļam, kā arī, lai atrastu un ielādētu modeļus.
print(sys.path) # izvada direktoriju sarakstu (sistēmas ceļu), lai meklētu modeļus, kad tos importē, izmantojot python.
python_version = '.'.join(map(str, sys.version_info[:2])) # iegūst pašreizējo Python versiju, ko formatē virknē.
print(python_version)
#site_packages = '/var/www/dj/g python-path=/var/www/.cache/pypoetry/virtualenvs/dj-vtp8n0h9-py3.12/lib/python3.12/site-packages'
#site_packages = '/var/www/.cache/pypoetry/virtualenvs/dj-vtp8n0h9-py3.12/lib/python3.12/site-packages'

#site.addsitedir(site_packages)

from django.core.wsgi import get_wsgi_application # tiek importēta funkcija, lai iegūtu WSGI lietojumprogrammas objektu.

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'g.settings' # iestata sistēmas vides mainīgajā (to nodrošina - os.environ) Django iesatīšanas modeli, kas atrodas g projekta python failā "settings", ko Python Django izmanto, lai zinātu, kā darbojas lietjumprogramma. 
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "g.settings")



# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', '/var/www/dj/g/g/settings')

application = get_wsgi_application() # mainīgo application iestata kā WSGI lietojumprogrammas objektu.


