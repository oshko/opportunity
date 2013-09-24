'''

Some entities are composed of other ones. For the user, it can be a
pain if you simply display the form. Consider applying for a job. Yes
we want to record the date but critically we need to know the position
and the company. This program presents composite entities in
sequence. In this example, we first ask for the company, then the
position and finally record meta data(e.g., data and comments).

These utility functions allow us to present a sequence of forms(aka,
wizard) to the user. The state for each view in the wizard is stored
in a list. Each element in the list is a tuple that has view
name(string), template(dictionary) of the parameters and a
description.

These sequences are enumerated below.

This design relies on a handful of keywords.

* activity = (string) name of the wizard UI
* co_id = (int) uid for company which was created for the sequence.
* pos_id = (int) uid for position which was created for the sequence.
* per_id = (int) uid for contact which was created for the sequence.


Interview
company    /prospect/add
position   /position/add  co_id=<d>
contact      /contact/add   co_id=<d>, pos_id=<d>
interview  /interview/add co_id=<d>, pos_id=<d>, per_id=<d>

Apply
company    /prospect/add
position   /position/add  co_id=<d>
apply      /apply/add     co_id=<d>, pos_id=<d>

Networking
company    /prospect/add
networking /networking/add co_id=<d>

Conversation
contact       /contact/add      
conversation /conversation/add per_id=<d>

'''

from django.utils import six

import logging

if six.PY3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode

from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)

# parameter/value names based by initial GET request
NEW_ACTIVITY = 'newactivity'   # initial dispatch
APPLY = 'apply'                # possible activity value
COMPANY = 'company'            # possible activity value
CONVERSATION = 'conversation'  # possible activity value
CONTACT = 'contact'            # possible activity value
DASHBOARD = 'dashboard'        # possible activity value
INTERVIEW = 'interview'        # possible activity value
NETWORKING = 'networking'      # possible activity value
POSITION = 'position'          # possible activity value

'''
Key names for key/value pairs. They are stored in hidden fields in form
and used to set the proper defaults for composite entities.
'''
ACTIVITY = 'activity'          # key to store the wiz name
CO_ID = 'co_id'                # UID for company
POS_ID = 'pos_id'              # UID for position
PER_ID = 'per_id'              # UID for person(contact)

'''
index for tuple
'''
VIEW_INDEX = 0
PARAM_INDEX = 1
DESC_INDEX = 2


class Composite(object):
    _state = None             # state for wizard transitions
    _state_index = None       # current state
    _state_next_index = None  # index to next state
    _activity_name = None     # activity name
    _view_name = None
    _title = None             # set in subclass
    _expected_keys = None     # keys which are expected

    def __init__(self, view):
        self._view_name = None
        self._state_index = None
        self._state_next_index = None

        # select a list with the right tuple
        self._state_index = [i for i, x in enumerate(self._state) if x[VIEW_INDEX] == view]
        self._state_index = self._state_index[0]
        self._state_next_index = self._state_index + 1
        self._view_name = self._state[self._state_next_index][VIEW_INDEX]

    def set(self, session, key, value):
        '''
        Store value in key.
        '''
        # store in session for next view
        session[key] = value
        # store in dict to allow us to compute url params
        self._state[self._state_next_index][PARAM_INDEX][key] = value
        # if any values are stored in session, copy them.
        for k in self._expected_keys:
            if k in session:
                self._state[self._state_next_index][PARAM_INDEX][k] = session[k]

    def delete_keys(self, session):
        '''
        When the wizard completes, delete keys from session
        '''
        for k in self._expected_keys:
            if k in session:
                del session[k]

    def get_next_url(self):
        '''
        What is the url to the next view in the sequence?
        '''
        url = None
        if self._view_name == COMPANY:
            url = reverse('opportunity.tracker.views.companyEdit',
                                args=['add'])
        elif self._view_name == POSITION:
            url = reverse('opportunity.tracker.views.positionEdit',
                                args=['add'])
        elif self._view_name == CONTACT:
            url = reverse('opportunity.tracker.views.personEdit',
                                args=['add'])
        elif self._view_name == INTERVIEW:
            url = reverse('opportunity.tracker.views.interviewEdit',
                                args=['add'])
        elif self._view_name == APPLY:
            url = reverse('opportunity.tracker.views.applyForEdit',
                                args=['add'])
        elif self._view_name == NETWORKING:
            url = reverse('opportunity.tracker.views.networkingEdit',
                                args=['add'])
        elif self._view_name == CONVERSATION:
            url = reverse('opportunity.tracker.views.conversationEdit',
                                args=['add'])
        elif self._view_name == DASHBOARD:
            url = reverse('opportunity.tracker.views.dashboard')
        # append params if any
        params = self._state[self._state_next_index][PARAM_INDEX]
        if params:
            url = "{0}?{1}".format(url,
                                       urlencode(self._convert_to_tuple(params)))
        return url

    def get_title(self):
        '''
        get title for this wizard. 
        '''
        return self._title

    def get_description(self):
        '''
        get description of this wizard. 
        '''
        return self._state[self._state_index][DESC_INDEX]

    def _convert_to_tuple(self, dict):
        '''

        A dictionary is great for maintaining parameters but it is
        difficult to write a test because you can't predict the order
        of the parameters. Return a tuple which will ensure the order
        of the parameters

        '''
        params = []
        for t in iter(sorted(dict.items())):
            params.append(t)
        return params

    @staticmethod
    def factory(activity, view):
        '''
        Given the activity name, return the wiz object if one
        is defined. If none are defined, return None.
        '''
        obj = None
        if activity == APPLY:
            obj = Apply(view)
        elif activity == CONVERSATION:
            obj = Conversation(view)
        elif activity == INTERVIEW:
            obj = Interview(view)
        elif activity == NETWORKING:
            obj = Networking(view)
        return obj


class Interview(Composite):
    def __init__(self, view):
        self._activity_name = INTERVIEW
        self._title = "Interview Wizard"
        self._expected_keys = [CO_ID, POS_ID, PER_ID]
        self._state = [(NEW_ACTIVITY, {}, "Unk"),
                       (COMPANY, {ACTIVITY: INTERVIEW},
                        "With which company are you interview?"),
                       (POSITION, {ACTIVITY: INTERVIEW, CO_ID: None},
                        "For which position are you interviewing?"),
                       (CONTACT, {ACTIVITY: INTERVIEW,
                                  CO_ID: None,
                                  POS_ID: None},
                        "With whom will you be speeking?"),
                       (INTERVIEW, {ACTIVITY: INTERVIEW,
                                    CO_ID: None,
                                    POS_ID: None,
                                    PER_ID: None},
                        "When is the interview?"),
                       (DASHBOARD, {}, ""), ]
        super(Interview, self).__init__(view)


class Apply(Composite):
    def __init__(self, view):
        self._activity_name = APPLY
        self._title = 'Apply Wizard'
        self._expected_keys = [CO_ID, POS_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
                       (COMPANY, {ACTIVITY: APPLY},
                        'At which company did you apply?'),
                       (POSITION, {ACTIVITY: APPLY, CO_ID: None},
                        'For which position did you apply?'),
                       (APPLY, {ACTIVITY: APPLY,
                                CO_ID: None,
                                POS_ID: None},
                        'When did you apply?'),
                       (DASHBOARD, {}, ""), ]
        super(Apply, self).__init__(view)


class Conversation(Composite):
    def __init__(self, view):
        self._activity_name = CONVERSATION
        self._title = "Conversation Wizard"
        self._expected_keys = [PER_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
                       (CONTACT, {ACTIVITY: CONVERSATION},
                        "With whom did you speak?"),
                       (CONVERSATION, {ACTIVITY: CONVERSATION,
                                       PER_ID: None},
                        "When was the conversation?"),
                       (DASHBOARD, {}, ""), ]
        super(Conversation, self).__init__(view)


class Networking(Composite):
    def __init__(self, view):
        self._activity_name = NETWORKING
        self._title = 'Networking wizard'
        self._expected_keys = [CO_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
                       (COMPANY, {ACTIVITY: NETWORKING},
                        "Where is the newtorking venue?"),
                       (NETWORKING, {ACTIVITY: NETWORKING,
                                     CO_ID: None},
                        "When and where is the event? "),
                       (DASHBOARD, {}, ""), ]
        super(Networking, self).__init__(view)
