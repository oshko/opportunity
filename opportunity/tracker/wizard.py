'''

These utility functions allow us to present a sequence of forms(aka,
wizard) to the user. The state for each view in the wizard is stored
in a list. Each element in the list is a tuple that has view
name(string), template(dictionary) of the expected values and the key
to store the UID for the entity just saved.

'''
import logging
import six
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

# new hidden fields keys
KNOWN_HF_KEYS = [ACTIVITY, CO_ID, POS_ID, PER_ID]

'''
index for tuple 
'''
VIEW_INDEX = 0
PARAM_INDEX = 1
NEXT_INDEX = 2

class Composite():
    _state = None          # state for wizard transitions
    _state_index = None
    _activity_name = None  # activity name 
    _view_name = None
    _url = None 

    def __init__(self, view):
        self._view_name = None
        self._state_index = None

        # select a list with the right tuple
        self._state_index = [i for i, x in enumerate(self._state) if x[VIEW_INDEX] == view]
        self._state_index = self._state_index[0]
        self._state_index += 1
        self._view_name = self._state[self._state_index][VIEW_INDEX]

    def set(self, session, key, value):
        '''
        Store value in key. 
        '''
        # store in session for next view
        session[key] = value
        # store in dict to allow us to compute url params
        self._state[self._state_index][PARAM_INDEX][key] = value

    def get_url(self):
        self._url = None
        if self._view_name == COMPANY:
            self._url = reverse('opportunity.tracker.views.companyView',
                                args=['add'])
        elif self._view_name == POSITION:
            self._url = reverse('opportunity.tracker.views.positionView',
                                args=['add'])
        elif self._view_name == CONTACT:
            self._url = reverse('opportunity.tracker.views.personView',
                                args=['add'])
        elif self._view_name == INTERVIEW:
            self._url = reverse('opportunity.tracker.views.interviewView',
                                args=['add'])
        elif self._view_name == APPLY:
            self._url = reverse('opportunity.tracker.views.applyForView',
                                args=['add'])
        elif self._view_name == NETWORKING:
            self._url = reverse('opportunity.tracker.views.networkingView',
                                args=['add'])
        elif self._view_name == CONVERSATION:
            self._url = reverse('opportunity.tracker.views.conversationView',
                                args=['add'])
        return self._url

    @staticmethod
    def factory(activity, view):
        '''
        Given the activity name, return the right object.
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
        else:
            raise Exception("activity doesn't map to a know wizard")
        return obj


class Interview(Composite):
    def __init__(self, view):
        self._activity_name = INTERVIEW
        self._state = [(NEW_ACTIVITY, {}),
                       (COMPANY, {ACTIVITY: INTERVIEW}, CO_ID),
                       (POSITION, {ACTIVITY: INTERVIEW, CO_ID: None}, POS_ID),
                       (CONTACT, {ACTIVITY: INTERVIEW,
                                  CO_ID: None,
                                  POS_ID: None}, PER_ID),
                       (INTERVIEW, {ACTIVITY: INTERVIEW,
                                    CO_ID: None,
                                    POS_ID: None,
                                    PER_ID: None}, None),
                       (DASHBOARD, {}), ]
        super().__init__(view)

    def get_url(self):
        '''
        see definition in parent class.
        '''
        super().get_url()
        params =  self._state[self._state_index][PARAM_INDEX]
        return "{0}?{1}".format(self._url,
                                urlencode(params))

    def set(self, session, key, value):
        super().set(session, key, value)
        # retrieve keys stored in session
        for k in [CO_ID, POS_ID, PER_ID]:
            if k in session:
                self._state[self._state_index][PARAM_INDEX][k] = session[k]


class Apply(Composite):
    def __init__(self):
        self._activity_name = APPLY
        self._state = [(NEW_ACTIVITY, {}),
                       (COMPANY, {ACTIVITY: APPLY}, CO_ID),
                       (POSITION, {ACTIVITY: APPLY, CO_ID: None}, POS_ID),
                       (APPLY, {ACTIVITY: APPLY,
                                CO_ID: None,
                                POS_ID: None}, None),
                       (DASHBOARD, {}), ]


class Conversation(Composite):
    def __init__(self):
        self._activity_name = CONVERSATION
        self._state = [(NEW_ACTIVITY, {}),
                       (COMPANY, {ACTIVITY: CONVERSATION}, CO_ID),
                       (CONTACT, {ACTIVITY: CONVERSATION,
                                  CO_ID: None}, PER_ID),
                       (CONVERSATION, {ACTIVITY: CONVERSATION,
                                       CO_ID: None,
                                       PER_ID: None}, None),
                       (DASHBOARD, {}), ]


class Networking(Composite):
    def __init__(self):
        self._activity_name = NETWORKING
        self._state = [(NEW_ACTIVITY, {}),
                       (COMPANY, {ACTIVITY: NETWORKING}, CO_ID),
                       (NETWORKING, {ACTIVITY: NETWORKING,
                                     CO_ID: None}, None),
                       (DASHBOARD, {}), ]
