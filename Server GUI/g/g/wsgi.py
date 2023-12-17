"""
WSGI config for g project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys
import site
print(sys.path)
python_version = '.'.join(map(str, sys.version_info[:2]))
print(python_version)
#site_packages = '/var/www/dj/g python-path=/var/www/.cache/pypoetry/virtualenvs/dj-vtp8n0h9-py3.12/lib/python3.12/site-packages'
#site_packages = '/var/www/.cache/pypoetry/virtualenvs/dj-vtp8n0h9-py3.12/lib/python3.12/site-packages'

#site.addsitedir(site_packages)

from django.core.wsgi import get_wsgi_application

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'g.settings'
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "g.settings")



# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', '/var/www/dj/g/g/settings')

application = get_wsgi_application()


