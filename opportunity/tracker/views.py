from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

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

# welcome page 
def hello(request):
    return render_to_response('about.html')

# reference which may help the job seeker
def books(request):
    return render_to_response('books.html')

# dashboard - initially just display the companies
def dashboard(request):
    positions = Position.objects.all()
    conversation = Conversation.objects.all()
    return render_to_response('dashboard.html', 
                             {'position_list' : positions, 
                              'activity_list' : prettyNames,
                              'conversation_list' : conversation })

# form to enter company 
def company(request):
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

# form to enter a person
def person(request):
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

# form to enter a position
def position(request):
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

# display to create a new activity.
def newactivity(request):
    newURL = '/' + mapNameToFunction[request.GET['activity']] + '/'
    return HttpResponseRedirect(newURL)    

# form to enter an interview
def interview(request):
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

# form to enter for submitting an apply
def applyFor(request):
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

# form to document a networking event 
def networking(request):
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

# form - remember to thank people  
def gratitude(request):
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

# form to enter a conversation
def conversation(request):
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

