# -*- python -*-

import os, sys

sys.path.append( os.path.join( os.path.dirname(__file__) ) )

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_site.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
