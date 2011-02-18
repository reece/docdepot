from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from docdepot.views import *

# import Filer in order to pull in config from that library
sys.path += [os.path.join(
	os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
	'lib'
	)]
from DocDepot.Filer import Filer


urlpatterns = patterns('',
    # Example:
    # (r'^www/', include('www.foo.urls')),

    #('^$', 'redirect_to', {'url' : '/pubmed'}),

	(r'^pubmed', pubmed),				
	(r'^help', help),				
	(r'^login/', 'django.contrib.auth.views.login'),
	(r'^openid/', include('django_openid_auth.urls')),

	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
	 {'document_root': os.path.join(os.path.dirname(__file__),'static')}),

	(r'^docdepot/(?P<path>.*)$', 'django.views.static.serve',
	 {'document_root': Filer.files_path }),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
