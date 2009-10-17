from django.conf.urls.defaults import *

urlpatterns = patterns('purl.views',
    url(r'^(?P<url_token>[A-Za-z0-9]+)/$', 'short_url', name='url-redirect'),
)
