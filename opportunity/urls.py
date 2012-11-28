from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opportunity.views.home', name='home'),
    # url(r'^opportunity/', include('opportunity.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^prospect/', 'opportunity.tracker.views.company'),
    (r'^contact/', 'opportunity.tracker.views.person'),
    (r'^position/', 'opportunity.tracker.views.position'),
    (r'^newactivity/', 'opportunity.tracker.views.newactivity'), # dispatch 
    (r'^interview/', 'opportunity.tracker.views.interview'), # activity 
    (r'^apply/', 'opportunity.tracker.views.applyFor'), # activity
    (r'^networking/', 'opportunity.tracker.views.networking'), # activity
    (r'^conversation/', 'opportunity.tracker.views.conversation'), # activity
    (r'^dashboard/', 'opportunity.tracker.views.dashboard'),
    (r'^$','opportunity.tracker.views.about'),
    (r'^books/$','opportunity.tracker.views.books'),
    (r'^profile/$','opportunity.tracker.views.profileView'),
    (r'^pitch/$', 'opportunity.tracker.views.pitchView'),
    (r'^onlinePresence/$', 'opportunity.tracker.views.onlinePresenceView'),
    (r'^par/(?P<op>add)$', 'opportunity.tracker.views.parView'),
    (r'^par/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.parView'),
    (r'^par/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.parDelete'),
    (r'^login/$', 'opportunity.tracker.views.loginRequest'),
    (r'^logout/$', 'opportunity.tracker.views.logoutRequest'),
    (r'^register/$','opportunity.tracker.views.registration'),
)

# newactivity
