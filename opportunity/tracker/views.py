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

def manage(request):
    """ manage allows user to edit or delete people and companies """
    people = Person.objects.all()
    companies = Company.objects.all()
    return render_to_response('manage.html',            
            {'contact_list': people,'prospect_list': companies}, 
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
    activities = Activity.getAll()
    return render_to_response('dashboard.html', 
                             {'position_list' : positions, 
                              'activity_name_list' : prettyNames,
                              'activity_list' : activities }, 
		                      context_instance=RequestContext(request))

@login_required
def companyView(request, *args, **kwargs):
    """
    A form to enter information about the company.
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = CompanyForm(request.POST, 
                instance=Company.objects.get(pk=int(kwargs['id'])))
        else: 
            form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = CompanyForm(
                    instance=Company.objects.get(pk=int(kwargs['id'])))
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = CompanyForm()
    return render_to_response('tracker_form.html',
                           {'title': _("Company"), 
                            'desc': _("Record information about a prospective employer."), 
                            'activity_name_list' : prettyNames,
                            'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def companyDelete(request, *args, **kwargs):
    """
    Delete company.
    """
    rc = { 'id' : kwargs['id'], 'idName': 'prospect',
        'noElements' : "No prospective companies at this time." } 
    try:
        obj = Company.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Company.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponse(simplejson.dumps(rc))

@login_required
def personView(request, *args, **kwargs):
    """
    A form to enter information about a person of interest. 
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = PersonForm(request.POST, 
                instance=Person.objects.get(pk=int(kwargs['id'])))
        else: 
            form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = PersonForm(
                    instance=Person.objects.get(pk=int(kwargs['id'])))
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = PersonForm()
    return render_to_response('tracker_form.html', 
                           {'title': _("Person"), 
                           'desc': _("Record a contact you met on the job hunt."),
                           'activity_name_list' : prettyNames, 
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def personDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'idName': 'contact',
        'noElements' : "No people at this time." } 
    try:
        obj = Person.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Person.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponse(simplejson.dumps(rc))


@login_required
def positionView(request, *args, **kwargs):
    """
    A form to enter information about a position
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = PositionForm(request.POST, 
                instance=Position.objects.get(pk=int(kwargs['id'])))
        else: 
            form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = PositionForm(
                    instance=Position.objects.get(pk=int(kwargs['id'])))
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = PositionForm()
    return render_to_response('tracker_form.html', 
                           {'title': _("Position"), 
                           'desc': _("Record a position in which you are interested.."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def positionDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'idName': 'position',
        'noElements' : "No positions being tracked." } 
    try:
        obj = Position.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Position.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponse(simplejson.dumps(rc))

@login_required
def newactivity(request):
    """
    Display to create a new activity.
    """
    newURL = '/' + mapNameToFunction[request.GET['activity']] + '/add'
    return HttpResponseRedirect(newURL)    

@login_required
def interviewView(request, *args, **kwargs):
    """
    form to enter information about an interview
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = InterviewForm(request.POST, 
                instance=Interview.objects.get(pk=int(kwargs['id'])))
        else: 
            form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = InterviewForm(
                    instance=Interview.objects.get(pk=int(kwargs['id'])))
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = InterviewForm()
    return render_to_response('tracker_form.html', 
                          {'title': _("Interview"), 
                           'desc': _("Record a pertinent interview."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
			               context_instance=RequestContext(request))

@login_required
def interviewDelete(request, *args, **kwargs):
    try:
        obj = Interview.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Interview.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponseRedirect('/dashboard/')

@login_required
def applyForView(request, *args, **kwargs):
    """
    A form to enter for submitting an apply
    /apply/(?P<op>add) - a new application
    /apply/(?P<op>edit)/(?P<id>\d+) - edit apply with id.
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = ApplyForm(request.POST, 
                instance=Apply.objects.get(pk=int(kwargs['id'])))
        else: 
            form = ApplyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = ApplyForm(
                    instance=Apply.objects.get(pk=int(kwargs['id'])))
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = ApplyForm()
    return render_to_response('tracker_form.html', {'title': _("Apply"), 
                           'desc': _("Record information about a job for which you applied."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def applyForDelete(request, *args, **kwargs):
    """
    /apply/(?P<op>del)/(?P<id>\d+) - delete apply with id.
    """
    try:
        obj = Apply.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Apply.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponseRedirect('/dashboard/')

@login_required
def networkingView(request, *args, **kwargs):
    """
    A form to document a networking event 
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = NetworkingForm(request.POST, 
                instance=Networking.objects.get(pk=int(kwargs['id'])))
        else: 
            form = NetworkingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = NetworkingForm(
                    instance=Networking.objects.get(pk=int(kwargs['id'])))
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = NetworkingForm()
    return render_to_response('tracker_form.html', {'title': _("Networking"), 
                           'desc': _("Record information about a networking event."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def networkingDelete(request, *args, **kwargs):
    try:
        obj = Networking.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Networking.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponseRedirect('/dashboard/')

@login_required
def gratitudeView(request, *args, **kwargs):
    """
    A form to setup a reminder to thank someone.
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = GratitudeForm(request.POST, 
                instance=Gratitude.objects.get(pk=int(kwargs['id'])))
        else: 
            form = GratitudeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = GratitudeForm( 
                    instance=Gratitude.objects.get(pk=int(kwargs['id'])))
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = GratitudeForm()
    return render_to_response('tracker_form.html', {'title': _("Gratitude"), 
                           'desc': _("Remember to thank those people who've helped you along the way."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def gratitudeDelete(request, *args, **kwargs):
    try:
        obj = Gratitude.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Gratitude.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponseRedirect('/dashboard/')

@login_required
def conversationView(request, *args, **kwargs):
    """
    A form to document a pertinent conversation
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = ConversationForm(request.POST, 
                instance=Conversation.objects.get(pk=int(kwargs['id'])))
        else: 
            form = ConversationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = ConversationForm(
                    instance=Conversation.objects.get(pk=int(kwargs['id'])))
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = ConversationForm()
    return render_to_response('tracker_form.html', 
                           {'title': _("Conversation"), 
                           'desc': _("Record a pertinent conversation."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def conversationDelete(request, *args, **kwargs):
    try:
        obj = Conversation.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Conversation.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponseRedirect('/dashboard/')

@login_required
def pitchView(request, *args, **kwargs):
    """
    Record the elevator pitch.   
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            fi = Pitch.objects.get(pk=int(kwargs['id']))
            form = PitchForm(request.POST, 
                instance=fi, user = request.user.get_profile())
        else: 
            form = PitchForm(request.POST, user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/')
    else:
        if kwargs['op'] == 'edit':
            try:
                fi = Pitch.objects.get(pk=int(kwargs['id']))
                form = PitchForm(instance=fi, user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else: 
            form = PitchForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html',
            { 'title': "Elevator Pitch",
            'desc': "The elevator pitch allows you to convey your value proposition when you meet new people in person.",
            'activity_name_list' : prettyNames,
            'form': form},
		    context_instance=RequestContext(request))

@login_required
def pitchDelete(request, *args, **kwargs):
    """
    Delete a elevator pitch. 
    /pitch/(?P<op>del)/(?P<id>\d+) - delete pitch with id. 
    """
    rc = { 'id' : kwargs['id'], 'idName': 'pitch',
        'noElements' : "No elevator pitch." } 
    try:
        obj = Pitch.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Pitch.DoesNotExist: 
        # todo: add logging 
        #  we wanted to delete it anyway. ignoring and contining.   
        pass
    return HttpResponse(simplejson.dumps(rc))

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
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request)) 
@login_required
def onlinePresenceDelete(request, *args, **kwargs):
    """
    Delete a reference link. 
    /onlinePresence/(?P<op>del)/(?P<id>\d+) - delete link with id. 
    """
    rc = { 'id' : kwargs['id'], 
        'idName': 'presence',
        'noElements' : "There are no links to references at this time."} 
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
    rc = { 'id' : kwargs['id'],'idName': 'story', 
        'noElements' : "There are no links to PAR based stories at this time." } 
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
                           'activity_name_list' : prettyNames,
                           'form': form}, 
                           context_instance=RequestContext(request))    

@login_required
def profileView(request):
    """ 
    This is a profile page. It contains the elevator pitch and responses to 
    behavioral interview questions. 
    """
    profile_id = request.user.userprofile.id
    ref_list = OnlinePresence.objects.filter(user=profile_id)
    story_list = PAR.objects.filter(user=profile_id)
    pitch_list = Pitch.objects.filter(user=profile_id)
    return render_to_response('profile.html', { 'ref_list' : ref_list, 
            'story_list' : story_list, 'pitch_list' : pitch_list }, 
            context_instance=RequestContext(request))

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
