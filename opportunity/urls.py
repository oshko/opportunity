from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from opportunity.tracker.views import PositionCommentCreate, PositionCommentUpdate, PositionCommentDelete 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opportunity.views.home', name='home'),
    # url(r'^opportunity/', include('opportunity.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^prospect/(?P<op>existing)', 'opportunity.tracker.views.companyDispatch'),
    (r'^prospect/(?P<op>add)', 'opportunity.tracker.views.companyEdit'),
    (r'^prospect/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.companyEdit'),
    (r'^prospect/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.companyDelete'),

    (r'^contact/(?P<op>existing)', 'opportunity.tracker.views.personDispatch'),
    (r'^contact/(?P<op>add)$', 'opportunity.tracker.views.personEdit'),
    (r'^contact/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.personEdit'),
    (r'^contact/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.personDelete'),
    
    (r'^position/(?P<op>add)$', 'opportunity.tracker.views.positionEdit'),
    (r'^position/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.positionEdit'),
    (r'^position/(?P<op>active)/(?P<id>\d+)$', 'opportunity.tracker.views.positionActivation'),
    (r'^position/(?P<op>inactive)/(?P<id>\d+)$', 'opportunity.tracker.views.positionActivation'),
    (r'^position/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.positionDelete'),
    
    (r'^newactivity/', 'opportunity.tracker.views.newactivity'), # dispatch activity
    
    (r'^interview/(?P<op>add)$', 'opportunity.tracker.views.interviewEdit'), # add 
    (r'^interview/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.interviewEdit'), # edit
    (r'^interview/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.interviewDelete'), # delete 
    
    (r'^apply/(?P<op>add)$', 'opportunity.tracker.views.applyForEdit'), # add
    (r'^apply/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.applyForEdit'), # edit
    (r'^apply/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.applyForDelete'), # delete
    
    (r'^networking/(?P<op>add)$', 'opportunity.tracker.views.networkingEdit'), # add
    (r'^networking/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.networkingEdit'), # edit
    (r'^networking/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.networkingDelete'), # delete
        
    (r'^conversation/(?P<op>add)$', 'opportunity.tracker.views.conversationEdit'), # add
    (r'^conversation/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.conversationEdit'), # edit
    (r'^conversation/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.conversationDelete'), # del

    (r'^mentormeeting/(?P<op>add)$', 'opportunity.tracker.views.mentormeetingEdit'), # add
    (r'^mentormeeting/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.mentormeetingEdit'), # edit
    (r'^mentormeeting/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.mentormeetingDelete'), # del

    (r'^mentorship/(?P<op>add)$', 'opportunity.tracker.views.mentorshipEdit'), # add
    (r'^mentorship/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.mentorshipEdit'), # edit
    (r'^mentorship/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.mentorshipDelete'), # del

    (r'^lunch/(?P<op>add)$', 'opportunity.tracker.views.lunchEdit'),
    (r'^lunch/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.lunchEdit'),
    (r'^lunch/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.lunchDelete'),
    
    (r'^dashboard/$', 'opportunity.tracker.views.dashboard'),
    (r'^dashboard/(?P<mentee_id>\d+)$', 'opportunity.tracker.views.dashboard'),
    (r'^profile/$','opportunity.tracker.views.profileView'),
    (r'^profile/(?P<mentee_id>\d+)$','opportunity.tracker.views.profileView'),

    (r'^$','opportunity.tracker.views.toplevelView'),
    (r'^coordinator/$','opportunity.tracker.views.coordinatorView'),
    (r'^books/$','opportunity.tracker.views.books'),
    (r'^about/$','opportunity.tracker.views.about'),
    
    (r'^pitch/(?P<op>add)$', 'opportunity.tracker.views.pitchEdit'), 
    (r'^pitch/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.pitchEdit'),  
    (r'^pitch/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.pitchDelete'),  
    
    (r'^onlinePresence/(?P<op>add)$', 'opportunity.tracker.views.onlinePresenceEdit'),
    (r'^onlinePresence/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.onlinePresenceEdit'),
    (r'^onlinePresence/(?P<op>del)/(?P<id>\d+)$', 'opportunity.tracker.views.onlinePresenceDelete'),
    
    (r'^par/(?P<op>add)$', 'opportunity.tracker.views.parEdit'),
    (r'^par/(?P<op>edit)/(?P<id>\d+)$', 'opportunity.tracker.views.parEdit'),
    (r'^par/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+)$', 'opportunity.tracker.views.parDelete'),
    
    (r'^comment/add$', 'opportunity.tracker.views.dispatchCommentCreate'),

    (r'^login/$', 'opportunity.tracker.views.loginRequest'),
    (r'^logout/$', 'opportunity.tracker.views.logoutRequest'),
    (r'^register/$','opportunity.tracker.views.registration'),
    (r'^resetpassword/passwordsent$','django.contrib.auth.views.password_reset_done'),
    (r'^resetpassword/$','django.contrib.auth.views.password_reset'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)

urlpatterns += staticfiles_urlpatterns()
