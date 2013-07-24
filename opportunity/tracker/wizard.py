'''
These utility funtions allow us to present a sequence of forms(aka, wizard) to
the user. The state for each view in the wizard is stored in a tuple. Each
element in the tuple will be a view name(string) and template(dictionary) of
the expected values.
'''
import logging

from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)


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
        if next_cmd == 'company':
            url = reverse('opportunity.tracker.views.companyView')
        elif next_cmd == 'position':
            url = reverse('opportunity.tracker.views.positionView')
        elif next_cmd == 'contact':
            url = reverse('opportunity.tracker.views.personView')
        elif next_cmd == 'interview':
            url = reverse('opportunity.tracker.views.interviewView')
        elif next_cmd == 'apply':
            url = reverse('opportunity.tracker.views.applyForView')
        elif next_cmd == 'networking':
            url = reverse('opportunity.tracker.views.networkingView')
        elif next_cmd == 'conversation':
            url = reverse('opportunity.tracker.views.conversationView')
        return url

    @staticmethod
    def factory(activity):
        '''
        Given the activity name, return the right object.
        '''
        obj = None
        if activity == 'apply':
            obj = Apply()
        elif activity == 'conservation':
            obj = Conversation()
        elif activity == 'interview':
            obj = Interview()
        elif activity == 'networking':
            obj = Networking()
        else:
            raise Exception("activity doesn't map to a know wizard")
        return obj


class Interview(Composite):
    def __init__(self):
        self._state = [('newactivity', {}),
                       ('company', {'activity': 'interview'}),
                       ('position', {'activity': None, 'co_id': None}),
                       ('contact', {'activity': 'interview',
                                    'co_id': None,
                                    'pos_id': None}),
                       ('interview', {'activity': 'interview',
                                      'co_id': None,
                                      'pos_id': None,
                                      'per_id': None}),
                       ('dashboard', {}), ]


class Apply(Composite):
    def __init__(self):
        self._state = [('newactivity', {}),
                       ('company', {'activity': 'apply'}),
                       ('position', {'activity': 'apply', 'co_id': None}),
                       ('apply', {'activity': 'apply', 'co_id': None}),
                       ('dashbord', {}), ]


class Conversation(Composite):
    def __init__(self):
        self._state = [('newactivity', {}),
                       ('company', {'activity': 'conversation'}),
                       ('contact', {'activity': 'conversation',
                                    'co_id': None}),
                       ('conversation', {'activity': 'conversation',
                                         'co_id': None,
                                         'per_id': None}),
                       ('dashbord', {}), ]


class Networking(Composite):
    def __init__(self):
        self._state = [('newactivity', {}),
                       ('company', {'activity': 'networking'}),
                       ('networking', {'activity': 'networking',
                                       'co_id': None}),
                       ('dashbord', {}), ]
