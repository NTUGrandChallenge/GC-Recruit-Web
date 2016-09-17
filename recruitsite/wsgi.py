"""
WSGI config for recruitsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os, sys, site

from django.core.wsgi import get_wsgi_application

site.addsitedir('/home/ubuntu/GC-Recruit-Web/ENV/lib/python3.4/site-packages')

sys.path.append('/home/ubuntu/GC-Recruit-Web')
sys.path.append('/home/ubuntu/GC-Recruit-Web/recruitsite')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitsite.settings")

application = get_wsgi_application()
