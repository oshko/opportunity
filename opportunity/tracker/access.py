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

aRequester - is user profile id who wants access
aTarget - is user profile id owns the data.

'''
def may_access_control(aRequesterId, aTargetId):
    rc = False
    # find UserProfile for requestor
    user_req =  UserProfile.objects.get(pk=aRequesterId)
    if user_req.is_upglo_staff:
        # UpGlo staff can access any page. 
        rc = True
    elif aRequesterId == aTargetId:
        # Requester owns requested page 
        rc = True 
    else:
        # is there a mentorship relationship between aRequester and aTarget?
        m = Mentorship.objects.filter(
            jobseeker__id=aTargetId, 
            mentor__id=aRequesterId)
        if len(m) == 1: 
            rc = True
    return rc
