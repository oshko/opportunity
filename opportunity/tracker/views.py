'''

As always with django this defines the views for the application.
Wizards (or a sequence of forms) is more complex. See the wizard
module for more detail.

'''

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils import six

import json
import logging
import datetime

if six.PY3:
    from urllib.error import HTTPError as http_error
    from http.client import responses as http_responses
else:
    from urllib2 import HTTPError as http_error
    from httplib import responses as http_responses

import opportunity.tracker.wizard as wizard

from .forms import *
from .models import *
from .crunchbase import CrunchProxy


# The prettyNames are displayed to the user.
prettyNames = [_("Company"), _("Person"), _("Position"), _("Interview"),
               _("Applying"), _("Networking"), _("Mentor Meeting"),
               _("Lunch"), _("Conversation")]

MSG_EMPTY_ACTIVITY = "No activities logged yet."
logger = logging.getLogger(__name__)

# The prettyNames are keys this hash array which returns
#   the url for the object or activity you want to enter.
mapNameToFunction = {_("Company"): "prospect",
                     _("Person"): "contact",
                     _("Position"): "position",
                     _("Interview"): "interview",
                     _("Applying"): "apply",
                     _("Networking"): "networking",
                     _("Mentor Meeting"): "mentormeeting",
                     _("Lunch"): "lunch",
                     _("Conversation"): "conversation"}


def _get_user_id(request):
    '''
    return the user id for the job seeker.
    Return -1 if not a job seeker
    '''
    profile_id = -1
    if request.user.userprofile.role == request.user.userprofile.JOB_SEEKER:
        profile_id = request.user.userprofile.id
    return profile_id


def toplevelView(request):
    """ welcome page """
    if request.user.is_authenticated():
        user_profile = request.user.get_profile()
        view_str = 'opportunity.tracker.views.dashboard'
        if user_profile.is_upglo_staff:
            # redirect to coordinatorView
            view_str = 'opportunity.tracker.views.coordinatorView'
        return HttpResponseRedirect(reverse(view_str))
    else:
        # not logged in? tell them about the purpose of the site.
        return render_to_response('about.html',
                                  context_instance=RequestContext(request))

def about(request):
    """ references to books which may help the job seeker """
    return render_to_response('about.html', 
                              context_instance=RequestContext(request))

def books(request):
    """ references to books which may help the job seeker """
    return render_to_response('books.html',
                              context_instance=RequestContext(request))


@login_required
def coordinatorView(request, *args, **kwargs):
    """
    UpGlo staff use this view to get an overview of the
    how the relationship between mentor and job seeker is
    playing out.
    """

    user = request.user.get_profile()
    page = None
    options = {}
    if user.is_upglo_staff:
        page = 'coordinator.html'
        # Get all active mentorships
        mentorships = [m for m in Mentorship.objects.all() if m.is_active()]
        for m in mentorships:
            m.first_contact = False
            m.freq = 0
            mtgs = MentorMeeting.objects.filter(mentorship__id=m.id)
            for mtg in mtgs:
                if mtg.face_to_face:
                    m.first_contact = mtg.face_to_face
                # how many times per month did they meet?
                total = len(mtgs)
                days = (datetime.date.today() - m.startDate).days
                ave_days_in_month = 30
                if days < ave_days_in_month:
                    m.freq = total
                else:
                    m.freq = total / ((days / ave_days_in_month) + 1)
        options['mentorships'] = mentorships
    else:
        page = 'upglo_only.html'

    return render_to_response(page, options,
                              context_instance=RequestContext(request))


@login_required
def dashboard(request, *args, **kwargs):
    """
    This is the dashboard page.  Aggregates information about prosepctive
    employers and activities in which the job hunter is engaged.
    """
    profile_id = None
    mentee_id = None
    page = None
    page_options = {}
    society = None
    
    if 'mentee_id' in request.GET:
        try: 
            # should always be an int. 
            mentee_id = int(request.GET['mentee_id'])
        except:
            logger.error('mentee_id must be an int')
            mentee_id = None
    
    page_options = perm_and_params(request.user.userprofile, mentee_id)

    if page_options['perm_p']:
        page = 'dashboard.html'
        page_options['position_list_active'] = \
            Position.objects.filter(user=page_options['profile_id'], active=True)
        page_options['position_list_inactive'] = \
            Position.objects.filter(user=page_options['profile_id'], active=False)
        page_options['contact_list'] = \
            Person.objects.filter(user=page_options['profile_id'])
        page_options['prospect_list'] = \
            Company.objects.filter(user=page_options['profile_id'])
        page_options['activity_list'] = \
            Activity.getAll(page_options['profile_id'])
        page_options['society'] = secret_society(request.user.get_profile(),
            page_options['profile_id'])
        page_options['activity_name_list'] = prettyNames
    else:
        page = 'perm_problem.html'
        page_options['err_message'] = 'You do not have permission to access this page.'

    return render_to_response(page,
                              page_options,
                              context_instance=RequestContext(request))


@login_required
def profileView(request, *args, **kwargs):
    """
    This is a profile page. It contains the elevator pitch and responses to
    behavioral interview questions.
    """
    mentee_id = None
    page_options = {}
    
    if 'mentee_id' in request.GET:
        try: 
            # should always be an int. 
            mentee_id = int(request.GET['mentee_id'])
        except:
            logger.error('mentee_id must be an int')
            mentee_id = None

    page_options = perm_and_params(request.user.userprofile, mentee_id) 

    if page_options['perm_p']:
        page = 'profile.html'
        page_options['pitch_list'] = \
            Pitch.objects.filter(user=page_options['profile_id'])
        page_options['ref_list'] = \
            OnlinePresence.objects.filter(user=page_options['profile_id'])
        page_options['story_list'] = \
            PAR.objects.filter(user=page_options['profile_id'])
        page_options['society'] = \
            secret_society(
                request.user.get_profile(), 
                page_options['profile_id'])
    else: 
        page = 'perm_problem.html'
        page_options['err_message'] = 'You do not have permission to access this page.'
    return render_to_response(page,
                              page_options,
                              context_instance=RequestContext(request))


@login_required
def membersView(request, *args, **kwargs):
    page = 'members.html'
    page_options = {} 
    # get list of users
    page_options['people'] = UserProfile.objects.all()
    # subtracting existing Mentorship relations
    # mentee's 
    # mentor's
    return render_to_response(page,
                              page_options,
                              context_instance=RequestContext(request))

def populateCompany(company_model):
    """
    Populate a Company model. It is factored out of the companyView()
    method to make it easier to test.
    """
    company_data = {}
    try:
        crunch = CrunchProxy()
        company_data = crunch.get_company_details(company_model.name)
    except http_error as e:
        logging.error(str.format("HTTP Error: {0} - {1}", e.code,
                                 http_responses[e.code]))
        try:
            # Explicitly looking for company by this name failed.
            # Try a generic search for the company name
            company_data = crunch.generic_query(company_model.name)
            # returns a list. Look at 'namespace' keys with
            # the value of 'company'. There can be multiple values.
            # Decide which one to use.
            company_data = [x for x in company_data
                           if x['namespace'] == 'company']
            companyAlternates = None  # a list of companies the search up.
            if not company_data:
                # empty list. reset company_data
                company_data = {}
            elif len(company_data) == 1:
                company_data = company_data[0]
            else:
                companyAlternates = company_data[1:]
                company_data = company_data[0]
        except http_error as e:
            logging.error(str.format("HTTP Error: {0} - {1}",
                                     e.code, http_responses[e.code]))
            err_msg = e.read()
            if err_msg:
                err_msg = json.loads(err_msg)
                if 'error' in err_msg:
                    logging.error(str.format("API Error: {0} ",
                                             err_msg['error']))
        logging.warning(
            str.format("Company, {0}, not found in crunchbase."
                       "Ignoring and continuing.",
                       company_model.name))
    # ignore result if there was api error.
    if not 'error' in company_data:
        if 'name' in company_data:
            company_model.name = company_data['name']
        if 'homepage_url' in company_data:
            company_model.website = company_data['homepage_url']

        # todo: there can be multiple offices. For now we just use one.
        office = {}
        if 'offices' in company_data and company_data['offices']:
            office = company_data['offices'][0]
        if 'address1' in office and office['address1'] is not None:
            company_model.address = office['address1'].strip()
        if 'address2' in office and office['address2'] is not None:
            tmp = office['address2'].strip()
            if tmp is not None and len(tmp) > 0:
                company_model.address += ", " + tmp
        if 'city' in office and office['city'] is not None:
            company_model.city = office['city'].strip()
        if 'state_code' in office and office['state_code'] is not None:
            company_model.state_province = office['state_code'].strip()
        if 'country_code' in office and office['country_code'] is not None:
            company_model.country = office['country_code'].strip()
        if 'zip_code' in office and office['zip_code'] is not None:
            company_model.zipCode = office['zip_code'].strip()
    return company_model


@login_required
def companyDispatch(request, *args, **kwargs):
    '''
    When a users selects an existing company from a form,
    this function calls the next view in the sequence with
    the uid for the company.
    '''
    activity = None
    if wizard.ACTIVITY in request.GET:
        activity = request.GET[wizard.ACTIVITY]
    if wizard.CO_ID in request.GET:
        c_id = request.GET[wizard.CO_ID]
    wiz = wizard.Composite.factory(activity, wizard.COMPANY)
    wiz.set(request.session, wizard.CO_ID, c_id)
    return HttpResponseRedirect(wiz.get_next_url())


@login_required
def companyView(request, *args, **kwargs):
    """
    A form to enter information about the company.
    """
    title = "Company"
    description = "Record information about a prospective employer."
    activity = None
    companies = None
    if wizard.ACTIVITY in request.GET:
        activity = request.GET[wizard.ACTIVITY]

    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = CompanyForm(request.POST,
                               instance=Company.objects.get(
                                   pk=int(kwargs['id'])),
                               user=request.user.get_profile())
        else:
            form = CompanyForm(request.POST, user=request.user.get_profile())
        if form.is_valid():
            c = form.save()
            url = None
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.COMPANY)
                if wiz:
                    wiz.set(request.session, wizard.CO_ID, c.id)
                    url = wiz.get_next_url()
            if not url:
                url = reverse('opportunity.tracker.views.dashboard')
            return HttpResponseRedirect(url)
    else:
        if kwargs['op'] == 'edit':
            try:
                form = CompanyForm(
                    instance=Company.objects.get(pk=int(kwargs['id'])),
                    user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            wiz = None
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.COMPANY)
                if wiz:
                    title = wiz.get_title()
                    description = wiz.get_description()
            companies = Company.objects.filter(
                user=_get_user_id(request))
            co = Company()
            if wizard.COMPANY in request.GET:
                co.name = request.GET['company'].strip()
                populateCompany(co)

            form = CompanyForm(
                instance=co,
                user=request.user.get_profile())
    return render_to_response('company_form.html',
                              {'title': title,
                               'desc': description,
                               'company_list': companies,
                               'activity_name_list': prettyNames,
                               'activity': activity,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def companyDelete(request, *args, **kwargs):
    """
    Delete company.
    """
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': "No prospective companies at this time."}
    try:
        obj = Company.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Company.DoesNotExist:
        logging.warning(
            str.format("Deleting company object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def personDispatch(request, *args, **kwargs):
    '''
    When a users selects an existing person from a form,
    this function calls the next view in the sequence with
    the uid for that person.
    '''
    activity = None
    p_id = None
    if wizard.ACTIVITY in request.GET:
        activity = request.GET[wizard.ACTIVITY]
    if wizard.PER_ID in request.GET:
        p_id = request.GET[wizard.PER_ID]
    wiz = wizard.Composite.factory(activity, wizard.CONTACT)
    wiz.set(request.session, wizard.PER_ID, p_id)
    return HttpResponseRedirect(wiz.get_next_url())


@login_required
def personView(request, *args, **kwargs):
    """
    A form to enter information about a person of interest.
    """
    title = "Person"
    description = "Record a contact you met on the job hunt."
    activity = None
    if wizard.ACTIVITY in request.GET:
        activity = request.GET[wizard.ACTIVITY]

    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = PersonForm(request.POST,
                              instance=Person.objects.get(
                                  pk=int(kwargs['id'])),
                              user=request.user.get_profile())
        else:
            form = PersonForm(request.POST,
                              user=request.user.get_profile())
        if form.is_valid():
            p = form.save()
            url = None
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.CONTACT)
                if wiz:
                    wiz.set(request.session, wizard.PER_ID, p.id)
                    url = wiz.get_next_url()
            if not url:
                url = reverse('opportunity.tracker.views.dashboard')
            return HttpResponseRedirect(url)
    else:
        if kwargs['op'] == 'edit':
            try:
                form = PersonForm(
                    instance=Person.objects.get(pk=int(kwargs['id'])),
                    user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            wiz = None
            pobj = Person()
            people = Person.objects.filter(
                user=_get_user_id(request))
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.CONTACT)
                if wiz:
                    title = wiz.get_title()
                    description = wiz.get_description()
                if wizard.CO_ID in request.GET:
                    cobj = Company.objects.get(
                        pk=request.GET[wizard.CO_ID])
                    pobj.company = cobj
            form = PersonForm(user=request.user.get_profile())
    return render_to_response('person_form.html',
                              {'title': title,
                               'desc': description,
                               'people_list': people,
                               'activity': activity,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def personDelete(request, *args, **kwargs):
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': "No people at this time."}
    try:
        obj = Person.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Person.DoesNotExist:
        logging.warning(
            str.format("Deleting person object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
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
                             user=request.user.get_profile())
        else:
            form = LunchForm(request.POST,
                             user=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('opportunity.tracker.views.dashboard'))
    else:
        if kwargs['op'] == 'edit':
            try:
                form = LunchForm(
                    instance=Lunch.objects.get(pk=int(kwargs['id'])),
                    user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            form = LunchForm(user=request.user.get_profile())
    return render_to_response('tracker_form.html',
                              {'title': _("Lunch(or Coffee)"),
                               'desc': _("Having Lunch(or Coffee)? ."),
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def lunchDelete(request, *args, **kwargs):
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': MSG_EMPTY_ACTIVITY}
    try:
        obj = Lunch.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Lunch.DoesNotExist:
        logging.warning(
            str.format("Deleting lunch object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def positionView(request, *args, **kwargs):
    """
    A form to enter information about a position
    """
    title = "Position"
    description = "Record a position in which you are interested."
    activity = None
    if wizard.ACTIVITY in request.GET:
        activity = request.GET[wizard.ACTIVITY]

    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = PositionForm(request.POST,
                                instance=Position.objects.get(
                                    pk=int(kwargs['id'])),
                                user=request.user.get_profile())
        else:
            form = PositionForm(request.POST,
                                user=request.user.get_profile())
        if form.is_valid():
            pos = form.save()
            url = None
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.POSITION)
                if wiz:
                    wiz.set(request.session, wizard.POS_ID, pos.id)
                    url = wiz.get_next_url()
            if not url:
                url = reverse('opportunity.tracker.views.dashboard')
            return HttpResponseRedirect(url)
    else:
        if kwargs['op'] == 'edit':
            try:
                form = PositionForm(
                    instance=Position.objects.get(pk=int(kwargs['id'])),
                    user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            wiz = None
            pos = Position()
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.POSITION)
                if wiz:
                    title = wiz.get_title()
                    description = wiz.get_description()
                if wizard.CO_ID in request.GET:
                    cobj = Company.objects.get(
                        pk=request.GET[wizard.CO_ID])
                    pos.company = cobj
            form = PositionForm(
                instance=pos,
                user=request.user.get_profile())
    return render_to_response('tracker_form.html',
                              {'title': title,
                               'desc': description,
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))

@login_required
def positionActivation(request, *args, **kwargs):
    '''
    When applying for a position, we do not always get it. 
    The dashboard shows active and inactive positions on 
    separate tabs. When the user toggles betwen they two, this
    function is called. 
    '''
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': "No positions being tracked."}
    try: 
        obj = Position.objects.get(pk=int('id'))
        if kwargs['op'] == 'active':
            obj.active = True
            obj.save()
        elif kwargs['op'] == 'inactive':
            obj.active = False
            obj.save()
    except:
        logging.warning("unable to update active field for position")
    return HttpResponse(json.dumps(rc))

@login_required
def positionDelete(request, *args, **kwargs):
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': "No positions being tracked."}
    try:
        obj = Position.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Position.DoesNotExist:
        logging.warning(
            str.format("Deleting position object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "We wanted to delete it anyway. ignoring and contining.")
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
    wiz = wizard.Composite.factory(a, wizard.NEW_ACTIVITY)
    if wiz:
        newURL = wiz.get_next_url()
    else:
        newURL = '/' + a + '/add'
    return HttpResponseRedirect(newURL)


@login_required
def interviewView(request, *args, **kwargs):
    """
    form to enter information about an interview
    """
    title = "Interview"
    description = "Record a pertinent interview."
    activity = None
    if wizard.ACTIVITY in request.GET:
        activity = request.GET[wizard.ACTIVITY]

    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = InterviewForm(request.POST,
                                 instance=Interview.objects.get(
                                     pk=int(kwargs['id'])),
                                 user=request.user.get_profile())
        else:
            form = InterviewForm(request.POST,
                                 user=request.user.get_profile())
        if form.is_valid():
            form.save()
            url = None
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.INTERVIEW)
                if wiz:
                    # no need to call wiz.set() because this is the last
                    # in the sequence.
                    url = wiz.get_next_url()
            if not url:
                url = reverse('opportunity.tracker.views.dashboard')
            return HttpResponseRedirect(url)
    else:
        if kwargs['op'] == 'edit':
            try:
                form = InterviewForm(
                    instance=Interview.objects.get(pk=int(kwargs['id'])),
                    user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            wiz = None
            iobj = Interview()
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.INTERVIEW)
                if wiz:
                    title = wiz.get_title()
                    description = wiz.get_description()
                if wizard.PER_ID in request.GET:
                    per_obj = Person.objects.get(
                        pk=request.GET[wizard.PER_ID])
                    iobj.withWhom = per_obj
                if wizard.POS_ID in request.GET:
                    pos_obj = Position.objects.get(
                        pk=request.GET[wizard.POS_ID])
                    iobj.position = pos_obj
            form = InterviewForm(
                instance=iobj, user=request.user.get_profile())

    return render_to_response('tracker_form.html',
                              {'title': title,
                               'desc': description,
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def interviewDelete(request, *args, **kwargs):
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': MSG_EMPTY_ACTIVITY}
    try:
        obj = Interview.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Interview.DoesNotExist:
        logging.warning(
            str.format("Deleting interview object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def applyForView(request, *args, **kwargs):
    """
    A form to enter for submitting an apply
    /apply/(?P<op>add) - a new application
    /apply/(?P<op>edit)/(?P<id>\d+) - edit apply with id.
    """
    title = "Apply"
    description = "Record information about a job for which you applied."
    activity = None
    if wizard.ACTIVITY in request.GET:
        activity = request.GET[wizard.ACTIVITY]

    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = ApplyForm(request.POST,
                             instance=Apply.objects.get(pk=int(kwargs['id'])),
                             user=request.user.get_profile())
        else:
            form = ApplyForm(request.POST,
                             user=request.user.get_profile())
        if form.is_valid():
            form.save()
            url = None
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.APPLY)
                if wiz:
                    # no need to call wiz.set() because this is the last
                    # in the sequence.
                    url = wiz.get_next_url()
            if not url:
                url = reverse('opportunity.tracker.views.dashboard')
            return HttpResponseRedirect(url)
    else:
        if kwargs['op'] == 'edit':
            try:
                form = ApplyForm(
                    instance=Apply.objects.get(pk=int(kwargs['id'])),
                    user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            wiz = None
            app_obj = Apply()
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.APPLY)
                if wiz:
                    title = wiz.get_title()
                    description = wiz.get_description()
                if wizard.POS_ID in request.GET:
                    pos_obj = Position.objects.get(
                        pk=request.GET[wizard.POS_ID])
                    app_obj.position = pos_obj
            form = ApplyForm(
                instance=app_obj,
                user=request.user.get_profile())
    return render_to_response('tracker_form.html',
                              {'title': title,
                               'desc': description,
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def applyForDelete(request, *args, **kwargs):
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': MSG_EMPTY_ACTIVITY}
    try:
        obj = Apply.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Apply.DoesNotExist:
        logging.warning(
            str.format("Deleting apply object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "We wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def networkingView(request, *args, **kwargs):
    """
    A form to document a networking event
    """
    title = "Networking"
    description = "Record information about a networking event."
    activity = None
    if wizard.ACTIVITY in request.GET:
        activity = request.GET[wizard.ACTIVITY]

    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = NetworkingForm(request.POST,
                                  instance=Networking.objects.get(
                                      pk=int(kwargs['id'])),
                                  user=request.user.get_profile())
        else:
            form = NetworkingForm(request.POST,
                                  user=request.user.get_profile())
        if form.is_valid():
            form.save()
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.NETWORKING)
                if wiz:
                    # no need to call wiz.set() because this is the last
                    # in the sequence.
                    url = wiz.get_next_url()
            if not url:
                url = reverse('opportunity.tracker.views.dashboard')
            return HttpResponseRedirect(url)
    else:
        if kwargs['op'] == 'edit':
            try:
                form = NetworkingForm(
                    instance=Networking.objects.get(pk=int(kwargs['id'])),
                    user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            wiz = None
            net_obj = Networking()
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.NETWORKING)
                if wiz:
                    title = wiz.get_title()
                    description = wiz.get_description()
                if wizard.CO_ID in request.GET:
                    cobj = Company.objects.get(
                        pk=request.GET[wizard.CO_ID])
                    net_obj.venue = cobj
            form = NetworkingForm(
                instance=net_obj,
                user=request.user.get_profile())
    return render_to_response('tracker_form.html',
                              {'title': title,
                               'desc': description,
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def networkingDelete(request, *args, **kwargs):
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': MSG_EMPTY_ACTIVITY}
    try:
        obj = Networking.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Networking.DoesNotExist:
        logging.warning(
            str.format("Deleting networking object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def mentormeetingView(request, *args, **kwargs):
    """
    A form to setup a meeting with mentor.
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = MeetingMentorForm(request.POST,
                                     instance=MentorMeeting.objects.get(
                                         pk=int(kwargs['id'])),
                                     user=request.user.get_profile())
        else:
            form = MeetingMentorForm(request.POST,
                                     user=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('opportunity.tracker.views.dashboard'))
    else:
        if kwargs['op'] == 'edit':
            try:
                form = MeetingMentorForm(
                    instance=MentorMeeting.objects.get(pk=int(kwargs['id'])),
                    user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            form = MeetingMentorForm(user=request.user.get_profile())
    return render_to_response('tracker_form.html',
                              {'title': _("Mentor Meeting"),
                               'desc': _("A form to record a"
                                         " meeting with mentor."),
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def mentormeetingDelete(request, *args, **kwargs):
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': MSG_EMPTY_ACTIVITY}
    try:
        obj = MentorMeeting.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except MentorMeeting.DoesNotExist:
        logging.warning(
            str.format("Deleting MentorMeeting object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def mentorshipView(request, *args, **kwargs):
    """
    A form to setup a mentorship.
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = MentorshipForm(request.POST,
                                  instance=Mentorship.objects.get(
                                      pk=int(kwargs['id'])))
        else:
            form = MentorshipForm(request.POST)
        if form.is_valid():
            mentorship = form.save(commit=False)
            # set expiration dated based on the start date provided.
            duration = 5  # in months
            y = mentorship.startDate.year
            m = mentorship.startDate.month + duration
            d = mentorship.startDate.day
            if (m > 12):
                m = m % 12
                y += 1
            expiration = datetime.date(y, m, 1)
            # check if the start month has more days then the expiration month
            (dontcare, daysInThisMonth) = calendar.monthrange(y, m)
            if d >= daysInThisMonth:
                d = daysInThisMonth
            mentorship.expirationDate = expiration + datetime.timedelta(d - 1)
            mentorship.save()
            return HttpResponseRedirect(
                reverse('opportunity.tracker.views.dashboard'))
    else:
        if kwargs['op'] == 'edit':
            try:
                form = MentorshipForm(
                    instance=Mentorship.objects.get(pk=int(kwargs['id'])))
            except:
                return HttpResponseServerError("bad id")
        else:
            form = MentorshipForm()
    return render_to_response('tracker_form.html',
                              {'title': _("Mentorship"),
                               'desc': _("A form to create a mentorship."),
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def mentorshipDelete(request, *args, **kwargs):
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': MSG_EMPTY_ACTIVITY}
    try:
        obj = Mentorship.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Mentorship.DoesNotExist:
        logging.warning(
            str.format("Deleting Mentorship object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def conversationView(request, *args, **kwargs):
    """
    A form to setup a meeting with mentor.
    """
    title = "Conversation"
    description = "Record a pertinent conversation."
    activity = None
    if wizard.ACTIVITY in request.GET:
        activity = request.GET[wizard.ACTIVITY]

    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            form = ConversationForm(request.POST,
                                    instance=Conversation.objects.get(
                                        pk=int(kwargs['id'])),
                                    user=request.user.get_profile())
        else:
            form = ConversationForm(request.POST,
                                    user=request.user.get_profile())
        if form.is_valid():
            form.save()
            url = None
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.CONVERSATION)
                if wiz:
                    # no need to call wiz.set() because this is the last
                    # in the sequence.
                    url = wiz.get_next_url()
            if not url:
                url = reverse('opportunity.tracker.views.dashboard')
            return HttpResponseRedirect(url)
    else:
        if kwargs['op'] == 'edit':
            try:
                form = ConversationForm(
                    instance=Conversation.objects.get(pk=int(kwargs['id'])),
                    user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            wiz = None
            conv_obj = Conversation()
            if activity:
                wiz = wizard.Composite.factory(activity, wizard.CONVERSATION)
                if wiz:
                    title = wiz.get_title()
                    description = wiz.get_description()
                if wizard.PER_ID in request.GET:
                    per_obj = Person.objects.get(
                        pk=request.GET[wizard.PER_ID])
                    conv_obj.person = per_obj
            form = ConversationForm(user=request.user.get_profile())
    return render_to_response('tracker_form.html',
                              {'title': title,
                               'desc': description,
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def conversationDelete(request, *args, **kwargs):
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'noElements': MSG_EMPTY_ACTIVITY}
    try:
        obj = Conversation.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Conversation.DoesNotExist:
        logging.warning(
            str.format("Deleting conversation object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def pitchView(request, *args, **kwargs):
    """
    Record the elevator pitch.
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            pitch = Pitch.objects.get(pk=int(kwargs['id']))
            form = PitchForm(request.POST,
                             instance=pitch, user=request.user.get_profile())
        else:
            form = PitchForm(request.POST, user=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('opportunity.tracker.views.profileView'))
    else:
        if kwargs['op'] == 'edit':
            try:
                pitch = Pitch.objects.get(pk=int(kwargs['id']))
                form = PitchForm(instance=pitch,
                                 user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            form = PitchForm(user=request.user.get_profile())
    return render_to_response('tracker_form.html',
                              {'title': "Elevator Pitch",
                               'desc': "The elevator pitch allows you"
                               " to convey your value proposition when"
                               " you meet new people in person.",
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def pitchDelete(request, *args, **kwargs):
    """
    Delete a elevator pitch.
    /pitch/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+) - delete pitch with id.
    """
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'idName': 'pitch',
          'noElements': "No elevator pitch."}
    try:
        obj = Pitch.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except Pitch.DoesNotExist:
        logging.warning(
            str.format("Deleting pitch object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def onlinePresenceView(request, *args, **kwargs):
    """
    A form for Online Presence. See model for model detail.
    /onlinePresence/(?P<op>add) - add a new story
    /onlinePresence/(?P<op>edit)/(?P<id>\d+) - present link.
          populate form with id.
    """
    if request.method == 'POST':
        if kwargs['op'] == 'edit':
            fi = OnlinePresence.objects.get(pk=int(kwargs['id']))
            form = OnlinePresenceForm(request.POST,
                                      instance=fi,
                                      user=request.user.get_profile())
        else:
            form = OnlinePresenceForm(request.POST,
                                      user=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('opportunity.tracker.views.profileView'))
    else:
        if kwargs['op'] == 'edit':
            try:
                fi = OnlinePresence.objects.get(pk=int(kwargs['id']))
                form = OnlinePresenceForm(instance=fi,
                                          user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            form = OnlinePresenceForm(user=request.user.get_profile())
    return render_to_response('tracker_form.html',
                              {'title': _("Online Presence"),
                               'desc': _("Record a link pointing to"
                                         " your online presence."),
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


@login_required
def onlinePresenceDelete(request, *args, **kwargs):
    """
    Delete a reference link.
    /onlinePresence/(?P<op>del)/(?P<id>\d+) - delete link with id.
    """
    rc = {'id': kwargs['id'],
          'idName': 'presence',
          'noElements': "There are no links to references at this time."}
    try:
        obj = OnlinePresence.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except OnlinePresence.DoesNotExist:
        logging.warning(
            str.format("Deleting online presence object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def parDelete(request, *args, **kwargs):
    """
    Delete a PAR story.
    /par/(?P<op>del)/(?P<id>\d+)/(?P<divId>\w+) - delete story with id.
    """
    rc = {'id': kwargs['id'], 'divId': kwargs['divId'],
          'idName': 'story',
          'noElements': "There are no links to PAR"
          " based stories at this time."}
    try:
        obj = PAR.objects.get(pk=int(kwargs['id']))
        obj.delete()
    except PAR.DoesNotExist:
        logging.warning(
            str.format("Deleting PAR object id, {0}, failed.",
                       kwargs['id']))
        logging.warning(
            "we wanted to delete it anyway. ignoring and contining.")
    return HttpResponse(json.dumps(rc))


@login_required
def parView(request, *args, **kwargs):
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
                           instance=fi,
                           user=request.user.get_profile())
        else:
            # create a new one
            form = PARForm(request.POST,
                           user=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('opportunity.tracker.views.profileView'))
    else:
        if kwargs['op'] == 'edit':
            try:
                a = PAR.objects.get(pk=int(kwargs['id']))
                form = PARForm(instance=a, user=request.user.get_profile())
            except:
                return HttpResponseServerError("bad id")
        else:
            form = PARForm(user=request.user.get_profile())
    return render_to_response('tracker_form.html',
                              {'title': _("PAR - problem, action, result"),
                               'desc': _("Record a response to a behaviorial"
                                         " question in PAR format."),
                               'activity_name_list': prettyNames,
                               'form': form},
                              context_instance=RequestContext(request))


def registration(request):
    view_str = 'opportunity.tracker.views.profileView'
    if request.user.is_authenticated():
        user_profile = request.user.get_profile()
        if user_profile.is_upglo_staff:
            view_str = 'opportunity.tracker.views.coordinatorView'
        return HttpResponseRedirect(reverse(view_str))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            profile = user.get_profile()
            profile.title = form.cleaned_data['title']
            profile.role = form.cleaned_data['role']
            profile.save()
            if profile.role is profile.COORDINATOR:
                view_str = 'opportunity.tracker.views.coordinatorView'
            return HttpResponseRedirect(reverse(view_str))
        else:
            return render_to_response("register.html", {'form': form},
                                      context_instance=RequestContext(request))
    else:
        ''' Show user blank registration form '''
        form = RegistrationForm()
        return render_to_response("register.html", {'form': form},
                                  context_instance=RequestContext(request))


def loginRequest(request):
    view_str = 'opportunity.tracker.views.profileView'
    if request.user.is_authenticated():
        user_profile = request.user.get_profile()
        if user_profile.is_upglo_staff:
            view_str = 'opportunity.tracker.views.coordinatorView'
        return HttpResponseRedirect(reverse(view_str))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']
            userprofile = authenticate(username=username, password=password)
            if userprofile is not None:
                login(request, userprofile)
                if userprofile.get_profile().is_upglo_staff:
                    view_str = 'opportunity.tracker.views.coordinatorView'
                return HttpResponseRedirect(reverse(view_str))
            else:
                return render_to_response(
                    "login.html", {'form': form},
                    context_instance=RequestContext(request))
        else:
            return render_to_response("login.html", {'form': form},
                                      context_instance=RequestContext(request))
    else:
        ''' show login form '''
        form = LoginForm()
        return render_to_response("login.html", {'form': form},
                                  context_instance=RequestContext(request))


def logoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')
