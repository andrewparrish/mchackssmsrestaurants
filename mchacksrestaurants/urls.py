from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'main.views.test'),
	url(r'^search/?', 'main.views.search'),

	url(r'^science/$', 'twilios.views.science'),
	url(r'^wat/(?P<msg>.*)$', 'twilios.views.science2'),
	url(r'^preferences/$', 'main.views.preferences'),
    # Examples:
    # url(r'^$', 'mchacksrestaurants.views.home', name='home'),
    # url(r'^mchacksrestaurants/', include('mchacksrestaurants.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

)
