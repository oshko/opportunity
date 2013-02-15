from django.contrib.auth.models import User
from models import Mentorship, UserProfile

'''
This module is responsible for ensuring access control. UpGlo staff
can access any page. Mentors and job seekers can access there home page.
For mentors and job seekers to acess another page, they must be in 
a mentorship relationship.

'''


'''
can user with aRequester access a page for aTarget? 

aRequester - is username who wants access
aTarget - is username owns the data.

'''
def may_access_control(aRequester, aTarget):
    rc = False
    # find UserProfile for requestor
    user_req =  UserProfile.objects.filter(user__username=aRequester)
    if len(user_req) == 1 and user_req[0].is_upglo_staff:
        # UpGlo staff can access any page. 
        rc = True
    elif aRequester == aTarget:
        # Requester owns requested page 
        rc = True 
    else:
        # import pdb; pdb.set_trace()
        # is there a mentorship relationship between aRequester and aTarget?
        m = Mentorship.objects.filter(
            jobseeker__user__username=aTarget, 
            mentor__user__username=aRequester)
        if len(m) == 1: 
            rc = True
    return rc
