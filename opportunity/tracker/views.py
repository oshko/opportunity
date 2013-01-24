from django.utils.translation import ugettext as _
from django.http import HttpResponse,HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

import httplib
import json 
import logging
import urllib2

from forms import *
from models import *
from crunchbase import CrunchProxy

# The prettyNames are displayed to the user. 
prettyNames = [_("Company"), _("Person"), _("Position"), _("Interview"),
    _("Applying"), _("Networking"), _("Gratitude"), _("Lunch"), _("Conversation")]

MSG_EMPTY_ACTIVITY="No activities logged yet."
logger = logging.getLogger(__name__)

# The prettyNames are keys this hash array which returns 
#   the url for the object or activity you want to enter. 
mapNameToFunction = {_("Company") : "prospect",
                     _("Person") : "contact",
                     _("Position") : "position",
                     _("Interview") : "interview",
                     _("Applying") : "apply",
                     _("Networking") : "networking",
                     _("Gratitude") : "gratitude",
                     _("Lunch") : "lunch",
                     _("Conversation") : "conversation"}

def about(request):
    """ welcome page """
    return render_to_response('about.html', 
		    context_instance=RequestContext(request))

@login_required
def manage(request):
    """ manage allows user to edit or delete people and companies """
    profile_id = request.user.userprofile.id
    people = Person.objects.filter(user=profile_id)
    companies = Company.objects.filter(user=profile_id)
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
    profile_id = request.user.userprofile.id
    positions = Position.objects.filter(user=profile_id)
    people = Person.objects.filter(user=profile_id)
    companies = Company.objects.filter(user=profile_id)
    activities = Activity.getAll()
    activities.reverse()
    return render_to_response('dashboard.html', 
                             {'activity_name_list' : prettyNames,
                              'activity_list' : activities,
                              'contact_list': people,
                              'position_list' : positions, 
                              'prospect_list': companies }, 
		                      context_instance=RequestContext(request))

@login_required
def companyView(request, *args, **kwargs):
    """
    A form to enter information about the company.
    """
    companyData = None # results from crunchbase company search
    companyAlternates = None # if mulitple hits, alternates go here 
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = CompanyForm(request.POST, 
                instance=Company.objects.get(pk=int(kwargs['id'])),
                user = request.user.get_profile())
        else: 
            form = CompanyForm(request.POST,user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = CompanyForm(
                    instance=Company.objects.get(pk=int(kwargs['id'])), 
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else:
            co = Company()
            companyData = {}
            if 'company' in request.GET:
                co.name = request.GET['company'].strip()
                try: 
                    crunch = CrunchProxy()
                    companyData = crunch.getCompanyDetails(co.name)
                except urllib2.HTTPError as e:
                    logging.error(str.format("HTTP Error: {0} - {1}", e.code,  httplib.responses[e.code]))
                    err_msg = e.read()
                    if err_msg: 
                        err_msg = json.loads(err_msg)
                        if 'error' in err_msg: 
                            logging.error(str.format("API Error: {0} ", err_msg['error']))
                    try:
                        # explicit lookup of company by this name failed. 
                        # Try a generic search for the company name
                        companyData = crunch.genericQuery(co.name)
                        # returns a list. Look at 'namespace' keys with
                        # the value of 'company'. There can be multiple values.
                        # Decide which one to use. 
                        companyData = [x for x in companyData if x['namespace'] == u'company']
                        companyAlternates = None # a list of companies the search up. 
                        if not companyData:
                            # empty list. reset companyData
                            companyData = {}
                        elif len(companyData) == 1: 
                            companyData = companyData[0] 
                        else:
                            companyAlternates = companyData[1:]
                            companyData = companyData[0]
                    except urllib2.HTTPError as e:
                        logging.error(str.format("HTTP Error: {0} - {1}", e.code,  httplib.responses[e.code]))
                        err_msg = e.read()
                        if err_msg: 
                            err_msg = json.loads(err_msg)
                            if 'error' in err_msg: 
                                logging.error(str.format("API Error: {0} ", err_msg['error']))
                    logging.warning(str.format("Company, {0}, not found in crunchbase. Ignoring and continuing.", co.name))
                # ignore result if there was api error.
                if not 'error' in companyData: 
                    if 'name' in companyData:
                        co.name = companyData['name']
                    if 'homepage_url' in companyData:
                        co.website = companyData['homepage_url']

                    # todo: there can be multiple offices. For now we just use one. 
                    office = {} 
                    if 'offices' in companyData and companyData['offices']:
                        office = companyData['offices'][0]
                    if 'address1' in office and office['address1'] != None:
                        co.address = office['address1'].strip()
                    if 'address2' in office and office['address2'] != None:
                        tmp = office['address2'].strip()
                        if tmp is not None and len(tmp) > 0:
                            co.address += ", " + tmp
                    if 'city' in office and office['city'] != None:
                        co.city = office['city'].strip()
                    if 'state_code' in office and office['state_code'] != None:
                        co.state_province = office['state_code'].strip()
                    if 'country_code' in office and office['country_code'] != None:
                        co.country = office['country_code'].strip()
                    if 'zip_code'  in office and office['zip_code'] != None:
                        co.zipCode = office['zip_code'].strip()

            form = CompanyForm(
                instance=co, 
                user = request.user.get_profile())
    return render_to_response('company_form.html',
                           {'title': _("Company"), 
                            'desc': _("Record information about a prospective employer."), 
                            'activity_name_list' : prettyNames,
                            'alternate_co_list': companyAlternates,
                            'form': form}, 
		                   context_instance=RequestContext(request))



@login_required
def companyDelete(request, *args, **kwargs):
    """
    Delete company.
    """
    rc = { 'id' : kwargs['id'], 'divId':  kwargs['divId'],
        'noElements' : "No prospective companies at this time." } 
    try:
        obj = Company.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Company.DoesNotExist: 
        logging.warning(str.format("Deleting company object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

@login_required
def personView(request, *args, **kwargs):
    """
    A form to enter information about a person of interest. 
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = PersonForm(request.POST, 
                instance=Person.objects.get(pk=int(kwargs['id'])),
                user = request.user.get_profile())
        else: 
            form = PersonForm(request.POST,
                user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = PersonForm(
                    instance=Person.objects.get(pk=int(kwargs['id'])),
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = PersonForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', 
                           {'title': _("Person"), 
                           'desc': _("Record a contact you met on the job hunt."),
                           'activity_name_list' : prettyNames, 
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def personDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'divId': kwargs['divId'],
        'noElements' : "No people at this time." } 
    try:
        obj = Person.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Person.DoesNotExist: 
        logging.warning(str.format("Deleting person object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.") 
    return HttpResponse(json.dumps(rc))

@login_required
def lunchView(request, *args, **kwargs):
    """
    A form to enter information a lunch appointment. 
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = LunchForm(request.POST, 
                instance=Lunch.objects.get(pk=int(kwargs['id'])),
                user = request.user.get_profile())
        else: 
            form = LunchForm(request.POST,
                user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = LunchForm(
                    instance=Lunch.objects.get(pk=int(kwargs['id'])),
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = LunchForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', 
                           {'title': _("Lunch(or Coffee)"), 
                           'desc': _("Having Lunch(or Coffee)? ."),
                           'activity_name_list' : prettyNames, 
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def lunchDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'divId': kwargs['divId'],
        'noElements' : MSG_EMPTY_ACTIVITY } 
    try:
        obj = Lunch.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Lunch.DoesNotExist: 
        logging.warning(str.format("Deleting lunch object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

@login_required
def positionView(request, *args, **kwargs):
    """
    A form to enter information about a position
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = PositionForm(request.POST, 
                instance=Position.objects.get(pk=int(kwargs['id'])),
                user = request.user.get_profile())
        else: 
            form = PositionForm(request.POST,
                user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = PositionForm(
                    instance=Position.objects.get(pk=int(kwargs['id'])),
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = PositionForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', 
                           {'title': _("Position"), 
                           'desc': _("Record a position in which you are interested.."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def positionDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'divId': kwargs['divId'],
        'noElements' : "No positions being tracked." } 
    try:
        obj = Position.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Position.DoesNotExist: 
        logging.warning(str.format("Deleting position object id, {0}, failed." , kwargs['id']))
        logging.warning("We wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

@login_required
def newactivity(request):
    """
    Display to create a new activity.
    """
    if request.GET['activity'] in mapNameToFunction:
        a = mapNameToFunction[request.GET['activity']]
    else:
        a = request.GET['activity']
    newURL = '/' + a + '/add'
    return HttpResponseRedirect(newURL)    

@login_required
def interviewView(request, *args, **kwargs):
    """
    form to enter information about an interview
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = InterviewForm(request.POST, 
                instance=Interview.objects.get(pk=int(kwargs['id'])),
                user = request.user.get_profile())
        else: 
            form = InterviewForm(request.POST,
                user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = InterviewForm(
                    instance=Interview.objects.get(pk=int(kwargs['id'])),
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = InterviewForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', 
                          {'title': _("Interview"), 
                           'desc': _("Record a pertinent interview."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
			               context_instance=RequestContext(request))

@login_required
def interviewDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'divId': kwargs['divId'], 
        'noElements' : MSG_EMPTY_ACTIVITY } 
    try:
        obj = Interview.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Interview.DoesNotExist: 
        logging.warning(str.format("Deleting interview object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

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
                instance=Apply.objects.get(pk=int(kwargs['id'])),
                user = request.user.get_profile())
        else: 
            form = ApplyForm(request.POST,
                user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = ApplyForm(instance=Apply.objects.get(pk=int(kwargs['id'])),
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = ApplyForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', {'title': _("Apply"), 
                           'desc': _("Record information about a job for which you applied."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def applyForDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'divId': kwargs['divId'], 
        'noElements' : MSG_EMPTY_ACTIVITY } 
    try:
        obj = Apply.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Apply.DoesNotExist: 
        logging.warning(str.format("Deleting apply object id, {0}, failed." , kwargs['id']))
        logging.warning("We wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

@login_required
def networkingView(request, *args, **kwargs):
    """
    A form to document a networking event 
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = NetworkingForm(request.POST, 
                instance=Networking.objects.get(pk=int(kwargs['id'])),
                user = request.user.get_profile())
        else: 
            form = NetworkingForm(request.POST,
                user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = NetworkingForm(
                    instance=Networking.objects.get(pk=int(kwargs['id'])),
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = NetworkingForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', {'title': _("Networking"), 
                           'desc': _("Record information about a networking event."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def networkingDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'divId': kwargs['divId'], 
        'noElements' : MSG_EMPTY_ACTIVITY } 
    try:
        obj = Networking.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Networking.DoesNotExist: 
        logging.warning(str.format("Deleting networking object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

@login_required
def gratitudeView(request, *args, **kwargs):
    """
    A form to setup a reminder to thank someone.
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = GratitudeForm(request.POST, 
                instance=Gratitude.objects.get(pk=int(kwargs['id'])),
                user = request.user.get_profile())
        else: 
            form = GratitudeForm(request.POST,
                user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = GratitudeForm( 
                    instance=Gratitude.objects.get(pk=int(kwargs['id'])),
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = GratitudeForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', {'title': _("Gratitude"), 
                           'desc': _("Remember to thank those people who've helped you along the way."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def gratitudeDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'divId': kwargs['divId'], 
        'noElements' : MSG_EMPTY_ACTIVITY } 
    try:
        obj = Gratitude.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Gratitude.DoesNotExist: 
        logging.warning(str.format("Deleting gratitdue object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

@login_required
def conversationView(request, *args, **kwargs):
    """
    A form to document a pertinent conversation
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = ConversationForm(request.POST, 
                instance=Conversation.objects.get(pk=int(kwargs['id'])),
                user = request.user.get_profile())
        else: 
            form = ConversationForm(request.POST,
                user = request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        if kwargs['op'] == 'edit':
            try:
                form = ConversationForm(
                    instance=Conversation.objects.get(pk=int(kwargs['id'])),
                    user = request.user.get_profile())
            except: 
                return HttpResponseServerError("bad id")
        else:
            form = ConversationForm(user = request.user.get_profile())
    return render_to_response('tracker_form.html', 
                           {'title': _("Conversation"), 
                           'desc': _("Record a pertinent conversation."), 
                           'activity_name_list' : prettyNames,
                           'form': form}, 
		                   context_instance=RequestContext(request))

@login_required
def conversationDelete(request, *args, **kwargs):
    rc = { 'id' : kwargs['id'], 'divId': kwargs['divId'], 
        'noElements' : MSG_EMPTY_ACTIVITY } 
    try:
        obj = Conversation.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Conversation.DoesNotExist: 
        logging.warning(str.format("Deleting conversation object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

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
        logging.warning(str.format("Deleting pitch object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

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
        logging.warning(str.format("Deleting online presence object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

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
        logging.warning(str.format("Deleting PAR object id, {0}, failed." , kwargs['id']))
        logging.warning("we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))

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
