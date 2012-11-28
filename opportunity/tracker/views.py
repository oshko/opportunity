from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.http import HttpResponse,HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

from forms import *
from models import *

# The prettyNames are displayed to the user. 
prettyNames = [_("Company"), _("Person"), _("Position"), _("Interview"),
    _("Applying"), _("Networking"), _("Gratitude"), _("Conversation")]

# The prettyNames are keys this hash array which returns 
#   the url for the object or activity you want to enter. 
mapNameToFunction = {_("Company") : "prospect",
                     _("Person") : "contact",
                     _("Position") : "position",
                     _("Interview") : "interview",
                     _("Applying") : "apply",
                     _("Networking") : "networking",
                     _("Gratitude") : "gratitude",
                     _("Conversation") : "conversation"}

def about(request):
    """ welcome page """
    return render_to_response('about.html', 
		    context_instance=RequestContext(request))

def books(request):
    """ references to books which may help the job seeker """ 
    return render_to_response('books.html', 
		    context_instance=RequestContext(request))

@login_required
def dashboard(request):
    """
    This is the dashboard page.  Aggregates information about prosepctive
    employers and activities in which the job hunter is engaged. 
    """
    positions = Position.objects.all()
    conversation = Conversation.objects.all()
    return render_to_response('dashboard.html', 
                             {'position_list' : positions, 
                              'activity_list' : prettyNames,
                              'conversation_list' : conversation }, 
		                      context_instance=RequestContext(request))

@login_required
def company(request):
    """
    A form to enter information about the company.
    """
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = CompanyForm()
    return render_to_response('tracker_form.html',
                           {'title': _("Company"), 
                           'desc': _("Record information about a prospective employer."), 
                           'form': form}, 
		                   context_instance=RequestContext(request))
@login_required
def person(request):
    """
    A form to enter information about a person of interest. 
    """
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = PersonForm()
    return render_to_response('tracker_form.html', 
                           {'title': _("Person"), 
                           'desc': _("Record a contact you met on the job hunt."), 
                           'form': form}, 
		                   context_instance=RequestContext(request))
@login_required
def position(request):
    """
    A form to enter information about a position
    """
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = PositionForm()
    return render_to_response('tracker_form.html', 
                           {'title': _("Position"), 
                           'desc': _("Record a position in which you are interested.."), 
                           'form': form}, 
		                   context_instance=RequestContext(request))
@login_required
def newactivity(request):
    """
    Display to create a new activity.
    """
    newURL = '/' + mapNameToFunction[request.GET['activity']] + '/'
    return HttpResponseRedirect(newURL)    

@login_required
def interview(request):
    """
    form to enter information about an interview
    """
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = InterviewForm()
    return render_to_response('tracker_form.html', 
                          {'title': _("Interview"), 
                           'desc': _("Record a pertinent interview."), 
                           'form': form}, 
			               context_instance=RequestContext(request))

@login_required
def applyFor(request):
    """
    A form to enter for submitting an apply
    """
    if request.method == 'POST':
        form = ApplyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = ApplyForm()
    return render_to_response('tracker_form.html', {'title': _("Apply"), 
                           'desc': _("Record information about a job for which you applied."), 
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def networking(request):
    """
    A form to document a networking event 
    """
    if request.method == 'POST':
        form = NetworkingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = NetworkingForm()
    return render_to_response('tracker_form.html', {'title': _("Networking"), 
                           'desc': _("Record information about a networking event."), 
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def gratitude(request):
    """
    A form to setup a reminder to thank someone.
    """
    if request.method == 'POST':
        form = GratitudeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = GratitudeForm()
    return render_to_response('tracker_form.html', {'title': _("Gratitude"), 
                           'desc': _("Remember to thank those people who've helped you along the way."), 
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def conversation(request):
    """
    A form to document a pertinent conversation
    """
    if request.method == 'POST':
        form = ConversationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = ConversationForm()
    return render_to_response('tracker_form.html', 
                           {'title': _("Conversation"), 
                           'desc': _("Record a pertinent conversation."), 
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def onlinePresenceView(request, *args, **kwargs):
    """
    A form for Online Presence. See model for model detail. 
    /onlinePresence/(?P<op>add) - add a new story
    /onlinePresence/(?P<op>edit)/(?P<id>\d+) - present link. populate form with id.
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit': 
            fi = OnlinePresence.objects.get(pk=int(kwargs['id']))
            form = OnlinePresenceForm(request.POST, 
                instance=fi, user = request.user.get_profile())
        else:
            form = OnlinePresenceForm(request.POST, user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/')
    else:
        if kwargs['op'] == 'edit': 
            try: 
                fi = OnlinePresence.objects.get(pk=int(kwargs['id']))
                form = OnlinePresenceForm(instance=fi, 
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else: 
            form = OnlinePresenceForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', 
                           {'title': _("Online Presence"), 
                           'desc': _("Record a link pointing to your online presence."), 
                           'form': form}, 
		                   context_instance=RequestContext(request)) 
@login_required
def onlinePresenceDelete(request, *args, **kwargs):
    """
    Delete a reference link. 
    /onlinePresence/(?P<op>del)/(?P<id>\d+) - delete link with id. 
    """
    rc = { 'id' : kwargs['id'] } 
    # import pdb; pdb.set_trace()
    try:
        obj = OnlinePresence.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except OnlinePresence.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponse(simplejson.dumps(rc))

@login_required
def parDelete(request, *args, **kwargs):
    """
    Delete a PAR story. 
    /par/(?P<op>del)/(?P<id>\d+) - delete story with id. 
    """
    rc = { 'id' : kwargs['id'] } 
    # import pdb; pdb.set_trace()
    try:
        obj = PAR.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except PAR.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponse(simplejson.dumps(rc))

@login_required
def parView (request, *args, **kwargs):
    """
    A form for PAR. See model for model detail. two URLs map to this function.
    /par/(?P<op>add) - add a new story
    /par/(?P<op>edit)/(?P<id>\d+) - present story. populate form with id. 
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            # edit existing story
            fi = PAR.objects.get(pk=int(kwargs['id']))
            form = PARForm(request.POST, 
                instance=fi, user = request.user.get_profile())
        else:
            # create a new one 
            form = PARForm(request.POST, user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/')
    else:
        if kwargs['op'] == 'edit': 
            try: 
                a = PAR.objects.get(pk=int(kwargs['id']))
                form = PARForm(instance=a ,user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id") 
        else: 
            form = PARForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', 
                           {'title': _("PAR - problem, action, result"), 
                           'desc': _("Record a response to a behaviorial question in PAR format."), 
                           'form': form}, 
                           context_instance=RequestContext(request))    

@login_required
def parDelete(request, *args, **kwargs):
    """
    Delete a PAR story. 
    /par/(?P<op>del)/(?P<id>\d+) - delete story with id. 
    """
    rc = { 'id' : kwargs['id'] } 
    # import pdb; pdb.set_trace()
    try:
        obj = PAR.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except PAR.DoesNotExist: 
        # todo: add loging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponse(simplejson.dumps(rc))

@login_required
def profileView(request):
    """ 
    This is a profile page. It contains the elevator pitch and responses to 
    behavioral interview questions. 
    """
    profile_id = request.user.userprofile.id
    ref_list = OnlinePresence.objects.filter(user=profile_id)
    story_list = PAR.objects.filter(user=profile_id)
    #import pdb; pdb.set_trace()
    return render_to_response('profile.html', { 'ref_list' : ref_list, 
            'story_list' : story_list}, context_instance=RequestContext(request))

# TODO: need a user profile with which to associate the pitch 
@login_required
def pitchView(request):
    """
    Record the elevator pitch.   
    """
    if request.method == 'POST':
        return HttpResponseRedirect('/dashboard/')
    else:
        return render_to_response('pitch_form.html', 
		    context_instance=RequestContext(request))


# TODO: need a user profile with which to associate this story.
@login_required
def story(request): 
    """
    Record stories for behaviorial interviews. 
    """
    pass 

def registration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid(): 
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'])
            user.save()
            profile = user.get_profile()
            profile.title = form.cleaned_data['title'] 
            profile.save()
            return HttpResponseRedirect('/profile/')
        else:
            return render_to_response("register.html", {'form': form },
                context_instance=RequestContext(request))
    else:
        ''' Show user blank registration form '''
        form = RegistrationForm()
        return render_to_response("register.html",{'form': form }, 
		    context_instance=RequestContext(request))

def loginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            userprofile = authenticate(username=username, password=password); 
            if userprofile is not None:
                login(request, userprofile)
                return HttpResponseRedirect('/profile/')
            else: 
                return render_to_response("login.html", {'form' : form}, 
                    context_instance=RequestContext(request))
        else: 
            return render_to_response("login.html", {'form' : form}, 
                context_instance=RequestContext(request))
    else:
        ''' show login form ''' 
        form = LoginForm()
        return render_to_response("login.html", {'form' : form}, 
		    context_instance=RequestContext(request))

def logoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')
