'''
These utility funtions allow us to present a sequence of forms(aka, wizard) to
the user. The state for each view in the wizard is stored in a list. Each
element in the list is a tuple will be a view name(string) and
template(dictionary) of the expected values.
'''
import logging

from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)

# parameter/value names based by initial GET request
NEW_ACTIVITY = 'newactivity'   # initial dispatch
APPLY='apply'                  # possible activity value
COMPANY = 'company'            # possible activity value
CONVERSATION = 'conversation'  # possible activity value
CONTACT = 'contact'            # possible activity value
DASHBOARD = 'dashboard'        # possible activity value
INTERVIEW = 'interview'        # possible activity value
NETOWRKING = 'networking'      # possible activity value
POSITION = 'position'          # possible activity value

'''
Key names for key/value pairs. They are stored in hidden fields in form
and used to set the proper defaults for composite entities. 
'''
ACTIVITY='activity'            # key to store the wiz name
CO_ID = 'co_id'                # UID for company 
POS_ID = 'pos_id'              # UID for position
PER_ID = 'per_id'              # UID for person(contact)

class Composite():
    _state = None

    def get_state(self, view):
        '''
        Return a tuple which represents the state of the UI Wizard based
        on the view for that class. Return None if view didn't map to
        state.
        '''
        obj = None
        # select a list with the right tuple
        list_obj = [self._state[i+1] for i, x in enumerate(self._state) if x[0] == view]
        if len(list_obj) == 1:
            obj = list_obj[0]
        return obj

    @staticmethod
    def get_baseurl(next_cmd):
        url = None
        if next_cmd == COMPANY:
            url = reverse('opportunity.tracker.views.companyView')
        elif next_cmd == POSITION:
            url = reverse('opportunity.tracker.views.positionView')
        elif next_cmd == CONTACT:
            url = reverse('opportunity.tracker.views.personView')
        elif next_cmd == INTERVIEW:
            url = reverse('opportunity.tracker.views.interviewView')
        elif next_cmd == APPLY:
            url = reverse('opportunity.tracker.views.applyForView')
        elif next_cmd == 'networking':
            url = reverse('opportunity.tracker.views.networkingView')
        elif next_cmd == CONVERSATION:
            url = reverse('opportunity.tracker.views.conversationView')
        return url

    @staticmethod
    def factory(activity):
        '''
        Given the activity name, return the right object.
        '''
        obj = None
        if activity == APPLY:
            obj = Apply()
        elif activity == CONVERSATION:
            obj = Conversation()
        elif activity == INTERVIEW:
            obj = Interview()
        elif activity == NETOWRKING:
            obj = Networking()
        else:
            raise Exception("activity doesn't map to a know wizard")
        return obj


class Interview(Composite):
    def __init__(self):
        self._state = [(NEW_ACTIVITY, {}),
                       (COMPANY, {ACTIVITY: INTERVIEW}),
                       (POSITION, {ACTIVITY: None, CO_ID: None}),
                       (CONTACT, {ACTIVITY: INTERVIEW,
                                    CO_ID: None,
                                    POS_ID: None}),
                       (INTERVIEW, {ACTIVITY: INTERVIEW,
                                      CO_ID: None,
                                      POS_ID: None,
                                      PER_ID: None}),
                       (DASHBOARD, {}), ]


class Apply(Composite):
    def __init__(self):
        self._state = [(NEW_ACTIVITY, {}),
                       (COMPANY, {ACTIVITY: APPLY}),
                       (POSITION, {ACTIVITY: APPLY, CO_ID: None}),
                       (APPLY, {ACTIVITY: APPLY, CO_ID: None}),
                       (DASHBOARD, {}), ]


class Conversation(Composite):
    def __init__(self):
        self._state = [(NEW_ACTIVITY, {}),
                       (COMPANY, {ACTIVITY: CONVERSATION}),
                       (CONTACT, {ACTIVITY: CONVERSATION,
                                    CO_ID: None}),
                       (CONVERSATION, {ACTIVITY: CONVERSATION,
                                         CO_ID: None,
                                         PER_ID: None}),
                       (DASHBOARD, {}), ]


class Networking(Composite):
    def __init__(self):
        self._state = [(NEW_ACTIVITY, {}),
                       (COMPANY, {ACTIVITY: NETOWRKING}),
                       (NETOWRKING, {ACTIVITY: NETOWRKING,
                                       CO_ID: None}),
                       (DASHBOARD, {}), ]
