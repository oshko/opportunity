from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from forms import CompanyForm
from models import Company

from forms import PersonForm
from models import Person

from forms import PositionForm
from models import Position

from forms import InterviewForm
from models import Interview

from forms import ApplyForm
from models import Apply 

from forms import NetworkingForm
from models import Networking 

from forms import GratitudeForm
from models import Gratitude 

from forms import ConversationForm
from models import Conversation 

from forms import RegistrationForm
from models import UserProfile

from forms import LoginForm

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
def profileView(request):
    """ 
    This is a profile page. It contains the elevator pitch and responses to 
    behavioral interview questions. 
    """
    return render_to_response('profile.html', 
		    context_instance=RequestContext(request))

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
            profile.url = form.cleaned_data['url']
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
