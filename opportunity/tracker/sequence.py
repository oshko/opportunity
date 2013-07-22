'''
These utility funtions allow us to present a sequence of forms to the user.
'''

from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)


def compose_start_baseurl(new_activity):
    ret = None
    if new_activity == 'apply':
        ret = compose_apply_baseurl('newactivity')
    elif new_activity == 'conservation':
        ret = compose_conservation_baseurl('newactivity')
    elif new_activity == 'interview':
        ret = compose_interview_baseurl('newactivity')
    elif new_activity == 'networking':
        ret = compose_networking_baseurl('newactivity')

    return ret


def compose_apply_baseurl(view_name):
    seq = ['newactivity', 'company', 'position', 'apply']
    return _compose_next_baseurl(seq, view_name)


def compose_conversation_baseurl(viwe_name):
    seq = ['newactivity', 'company', 'contact', 'conversation']
    return _compose_next_baseurl(seq, view_name)


def compose_interview_baseurl(view_name):
    seq = ['newactivity', 'company', 'position',
           'contact', 'interview', 'dashboard']
    return _compose_next_baseurl(seq, view_name)


def compose_networking_baseurl(view_name):
    seq = ['newactivity', 'company', 'networking']
    return _compose_next_baseurl(seq, view_name)


def _compose_next_baseurl(seq, view_name):
    '''
    This is a utility function to compute the next view in a
    sequence.
    '''
    url = None

    # what is the next view?
    try:
        view_index = seq.index(view_name)
        view_index += 1
    except:
        view_index = None
        logger.error(
            "next view {0} not found in "
            " Interview Sequence".format(view_name))
        next_view = None
    if view_index is not None and view_index < len(seq):
        next_view = seq[view_index]
    else:
        logger.error("Out of range Interview Sequence")
        view_index = -1
        next_view = 'dashboard'

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
