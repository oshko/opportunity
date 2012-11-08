from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

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

# The prettyNames are displayed to the user. 
prettyNames = ["Company","Person","Position","Interview","Applying","Networking","Gratitude","Conversation"]

# The prettyNames are keys this hash array which returns 
#   the url for the object or activity you want to enter. 
mapNameToFunction = {"Company" : "prospect",
                     "Person" : "contact",
                     "Position" : "position",
                     "Interview" : "interview",
                     "Applying" : "apply",
                     "Networking" : "networking",
                     "Gratitude" : "gratitude",
                     "Conversation" : "conversation"}

def hello(request):
    """ welcome page """
    return render_to_response('about.html')

def books(request):
    """ references to books which may help the job seeker """ 
    return render_to_response('books.html')

def profile(request):
    """ 
    This is a profile page. It contains the elevator pitch and responses to 
    behavioral interview questions. 
    """
    return render_to_response('profile.html')

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
                              'conversation_list' : conversation })

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
                           {'title': "Company", 
                           'desc': "Record information about a prospective employer.", 
                           'form': form})

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
                           {'title': "Person", 
                           'desc': "Record a contact you met on the job hunt.", 
                           'form': form})

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
                           {'title': "position", 
                           'desc': "Record a position in which you are interested..", 
                           'form': form})

def newactivity(request):
    """
    Display to create a new activity.
    """
    newURL = '/' + mapNameToFunction[request.GET['activity']] + '/'
    return HttpResponseRedirect(newURL)    

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
                          {'title': "Interview", 
                           'desc': "Record a pertinent interview.", 
                           'form': form})

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
    return render_to_response('tracker_form.html', {'title': "Apply", 
                           'desc': "Record information about a job for which you applied.", 
                           'form': form})

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
    return render_to_response('tracker_form.html', {'title': "Networking", 
                           'desc': "Record information about a networking event.", 
                           'form': form})

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
    return render_to_response('tracker_form.html', {'title': "Gratitude", 
                           'desc': "Remember to thank those people who've helped you along the way.", 
                           'form': form})

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
                           {'title': "Conversation", 
                           'desc': "Record a pertinent conversation.", 
                           'form': form})
# TODO: need a user profile with which to associate the pitch 
def pitch(request):
    """
    Record the elevator pitch.   
    """
    if request.method == 'POST':
        return HttpResponseRedirect('/pitch/')
    else:
        return render_to_response('pitch_form.html')


# TODO: need a user profile with which to associate this story.
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
            return render_to_response("register.html", {'form': form }, context_instance=RequestContext(request))
    else:
        ''' Show user blank registration form '''
        form = RegistrationForm()
        return render_to_response("register.html",{'form': form }, context_instance=RequestContext(request))
