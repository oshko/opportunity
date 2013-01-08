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
    (r'^prospect/(?P<op>add)$', 'opportunity.tracker.views.companyView'),
    (r'^prospect/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.companyView'),
    (r'^prospect/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.companyDelete'),
    
    (r'^contact/(?P<op>add)$', 'opportunity.tracker.views.personView'),
    (r'^contact/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.personView'),
    (r'^contact/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.personDelete'),
    
    (r'^position/(?P<op>add)$', 'opportunity.tracker.views.positionView'),
    (r'^position/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.positionView'),
    (r'^position/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.positionDelete'),
    
    (r'^newactivity/', 'opportunity.tracker.views.newactivity'), # dispatch activity
    
    (r'^interview/(?P<op>add)$', 'opportunity.tracker.views.interviewView'), # add 
    (r'^interview/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.interviewView'), # edit
    (r'^interview/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.interviewDelete'), # delete 
    
    (r'^apply/(?P<op>add)$', 'opportunity.tracker.views.applyForView'), # add
    (r'^apply/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.applyForView'), # edit
    (r'^apply/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.applyForDelete'), # delete
    
    (r'^networking/(?P<op>add)$', 'opportunity.tracker.views.networkingView'), # add
    (r'^networking/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.networkingView'), # edit
    (r'^networking/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.networkingDelete'), # delete
    
    (r'^gratitude/(?P<op>add)$', 'opportunity.tracker.views.gratitudeView'), # add
    (r'^gratitude/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.gratitudeView'), # activity
    (r'^gratitude/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.gratitudeDelete'), # activity
    
    (r'^conversation/(?P<op>add)$', 'opportunity.tracker.views.conversationView'), # add
    (r'^conversation/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.conversationView'), # edit
    (r'^conversation/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.conversationDelete'), # del
    
    (r'^dashboard/', 'opportunity.tracker.views.dashboard'),
    (r'^$','opportunity.tracker.views.about'),
    (r'^books/$','opportunity.tracker.views.books'),
    (r'^profile/$','opportunity.tracker.views.profileView'),
    (r'^pitch/(?P<op>add)$', 'opportunity.tracker.views.pitchView'), 
    (r'^pitch/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.pitchView'),  
    (r'^pitch/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.pitchDelete'),  
    (r'^onlinePresence/(?P<op>add)$', 'opportunity.tracker.views.onlinePresenceView'),
    (r'^onlinePresence/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.onlinePresenceView'),
    (r'^onlinePresence/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.onlinePresenceDelete'),
    (r'^par/(?P<op>add)$', 'opportunity.tracker.views.parView'),
    (r'^par/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.parView'),
    (r'^par/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.parDelete'),
    (r'^login/$', 'opportunity.tracker.views.loginRequest'),
    (r'^logout/$', 'opportunity.tracker.views.logoutRequest'),
    (r'^register/$','opportunity.tracker.views.registration'),
    (r'^password_change/$','django.contrib.auth.views.password_change'),
    (r'^password_reset/$','django.contrib.auth.views.password_reset'),
    
)

# newactivity
