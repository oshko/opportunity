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
comment    /comment/add int_id=<d>

Apply
company    /prospect/add
position   /position/add  co_id=<d>
apply      /apply/add     co_id=<d>, pos_id=<d>
comment    /comment/add apply_id=<d>

Networking
company    /prospect/add
networking /networking/add co_id=<d>
comment    /comment/add net_id=<d>

Conversation
contact       /contact/add      
conversation /conversation/add per_id=<d
comment    /comment/add conv_id=<d>

Add company 
company    /prospect/add
comment    /comment/add co_id=<d>

Add Position 
position   /position/add  
comment    /comment/add pos_id=<d>

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
MENTORMTG = 'mentormtg'        # possible activity value
ADD_COMPANY = 'add_company'
ADD_POSITION = 'add_position' 
COMMENT = 'comment'

'''
Key names for key/value pairs. They are stored in hidden fields in form
and used to set the proper defaults for composite entities.
'''
ACTIVITY = 'activity'          # key to store the wiz name
CO_ID = 'co_id'                # UID for company
POS_ID = 'pos_id'              # UID for position
PER_ID = 'per_id'              # UID for person (contact)
APP_ID = 'app_id'              # UID for apply
CONV_ID = 'conv_id'            # UID for conversation
INT_ID = 'int_id'              # UID for interview 
MENT_ID = 'ment_id'            # UID for mentor meeting
NET_ID = 'net_id'              # UID for networking

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
        elif self._view_name == COMMENT:
            url = reverse('opportunity.tracker.views.dispatchCommentCreate')
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

    def is_prospective(self):
        '''
        Sometimes we are interseted in companies as prospective
        employers. Other times they are networking venues. Return true
        if this activity is recording a prospective employer else false.
        '''
        rc = False
        if self._activity_name in [ADD_COMPANY, ADD_POSITION, APPLY, INTERVIEW]:
            rc = True
        return rc

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
        elif activity == ADD_COMPANY:
            obj = AddCompany(view)
        elif activity == ADD_POSITION:
            obj = AddPosition(view)
        return obj


class Interview(Composite):
    def __init__(self, view):
        self._activity_name = INTERVIEW
        self._title = "Interview Wizard"
        self._expected_keys = [CO_ID, INT_ID, POS_ID, PER_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
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
                       (COMMENT, {ACTIVITY: INTERVIEW,
                                  INT_ID: None
                                  },
                        "Any comments about this interview?"),
                       (DASHBOARD, {}, ""), ]
        super(Interview, self).__init__(view)


class Apply(Composite):
    def __init__(self, view):
        self._activity_name = APPLY
        self._title = 'Apply Wizard'
        self._expected_keys = [APP_ID, CO_ID, POS_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
                       (COMPANY, {ACTIVITY: APPLY},
                        'At which company did you apply?'),
                       (POSITION, {ACTIVITY: APPLY, CO_ID: None},
                        'For which position did you apply?'),
                       (APPLY, {ACTIVITY: APPLY,
                                CO_ID: None,
                                POS_ID: None},
                        'When did you apply?'),
                       (COMMENT, {ACTIVITY: APPLY,
                                  APP_ID: None
                                  }, 
                        "Any comments about this interview?"),
                       (DASHBOARD, {}, ""), ]
        super(Apply, self).__init__(view)


class Conversation(Composite):
    def __init__(self, view):
        self._activity_name = CONVERSATION
        self._title = "Conversation Wizard"
        self._expected_keys = [PER_ID, CONV_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
                       (CONTACT, {ACTIVITY: CONVERSATION},
                        "With whom did you speak?"),
                       (CONVERSATION, {ACTIVITY: CONVERSATION,
                                       PER_ID: None},
                        "When was the conversation?"),
                       (COMMENT, {ACTIVITY: CONVERSATION,
                                  CONV_ID: None},
                        "Any comments about this conversation?"),
                       (DASHBOARD, {}, ""), ]
        super(Conversation, self).__init__(view)


class Networking(Composite):
    def __init__(self, view):
        self._activity_name = NETWORKING
        self._title = 'Networking wizard'
        self._expected_keys = [CO_ID, NET_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
                       (COMPANY, {ACTIVITY: NETWORKING},
                        "Where is the newtorking venue?"),
                       (NETWORKING, {ACTIVITY: NETWORKING,
                                     CO_ID: None},
                        "When and where is the event? "),
                       (COMMENT, {ACTIVITY: NETWORKING,
                                  NET_ID: None}, 
                        "Any comments about this Networking event?"),
                       (DASHBOARD, {}, ""), ]
        super(Networking, self).__init__(view)

class MentorMeeting(Composite):
    def __init__(self, view):
        self._activity_name = MENTORMTG
        self._title = 'Mentor Meeting wizard'
        self._expected_keys = [CO_ID, MENT_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
                       (MENTORMTG, {ACTIVITY: MENTORMTG }, 
                        "Mentor meeting"),
                       (COMMENT, {ACTIVITY: ADD_COMPANY,
                                     MENT_ID: None},
                        "Any comments about this meeting? "),
                       (DASHBOARD, {}, ""), ]
        super(MentorMeeting, self).__init__(view)

class AddCompany(Composite):
    def __init__(self, view):
        self._activity_name = ADD_COMPANY
        self._title = 'Add Company wizard'
        self._expected_keys = [CO_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
                       (COMPANY, {ACTIVITY: ADD_COMPANY},
                        "Record pertainent information about this company."),
                       (COMMENT, {ACTIVITY: ADD_COMPANY,
                                     CO_ID: None},
                        "Any comments about this company you'd like to record? "),
                       (DASHBOARD, {}, ""), ]
        super(AddCompany, self).__init__(view)


class AddPosition(Composite):
    def __init__(self, view):
        self._activity_name = ADD_POSITION
        self._title = 'Add Position wizard'
        self._expected_keys = [POS_ID]
        self._state = [(NEW_ACTIVITY, {}, ""),
                       (POSITION, {ACTIVITY: ADD_POSITION},
                        "Record pertainent information about this position."),
                       (COMMENT, {ACTIVITY: ADD_POSITION,
                                     POS_ID: None},
                        "Any comments about this position you'd like to record? "),
                       (DASHBOARD, {}, ""), ]
        super(AddPosition, self).__init__(view)
