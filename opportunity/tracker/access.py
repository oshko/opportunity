'''
This module is responsible for ensuring access control. UpGlo staff
can access any page. Mentors and job seekers can access there home page.
For mentors and job seekers to acess another page, they must be in
a mentorship relationship.

'''
from django.contrib.auth.models import User
from .models import Mentorship, UserProfile


def may_access_control(requester_id, target_id):
    '''
    can user with requester_id access a page for target_id?

    requester_id - is user profile id who wants access
    target_id - is user profile id owns the data.

    '''
    ret = False
    # find UserProfile for requestor
    user_req = UserProfile.objects.get(pk=requester_id)
    if user_req.is_upglo_staff:
        # UpGlo staff can access any page.
        ret = True
    elif requester_id == target_id:
        # Requester owns requested page
        ret = True
    else:
        # is there a mentorship relationship between aRequester and aTarget?
        m_rel = Mentorship.objects.filter(
            jobseeker__id=target_id,
            mentor__id=requester_id)
        if len(m_rel) == 1:
            ret = True
    return ret
