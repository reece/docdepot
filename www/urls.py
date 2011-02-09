from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from docdepot.views import *

urlpatterns = patterns('',
    # Example:
    # (r'^www/', include('www.foo.urls')),
					   
	(r'^pubmed/$', pubmed),				
	(r'^login/', 'django.contrib.auth.views.login'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
