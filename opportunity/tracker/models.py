from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

import calendar 
import datetime

class UserProfile(models.Model):
    """
    A UserProfile is a person which uses our system.
    """
    user = models.OneToOneField(User)
    title = models.CharField(max_length=32) 
    is_upglo_staff = models.BooleanField(default=False)
    JOB_SEEKER = "jobseeker"
    MENTOR = "mentor"
    COORDINATOR = "coordinator"
    ROLES_AT_UPGLO = (
        (JOB_SEEKER, "Job seeker"), 
        (MENTOR, "Mentor"), 
        (COORDINATOR, "Coordinator"),
    )
    role = models.CharField(max_length=12, 
        choices=ROLES_AT_UPGLO,
        default=JOB_SEEKER)

    def __unicode__(self):
        return self.user.username

# UserProfile is associated with the User table. Listen for the post_save 
# signal. Create a profile when new User added.

def create_user_profile(sender, instance, created, **kwargs):
    """
    This is the callback associated with the post_save signal on User. 	
    """ 
    if created:
        UserProfile.objects.create(user=instance)

# register for post_save signal on User 
post_save.connect(create_user_profile, sender=User)

"""
A mentor assists a mentee with respect to finding a job.
UpGlo Mentorships last five months.
"""
class Mentorship(models.Model):
    jobseeker = models.ForeignKey(UserProfile,related_name='jobseeker')
    mentor = models.ForeignKey(UserProfile, related_name='mentor')
    startDate =  models.DateField() # should be set in UI
    expirationDate = models.DateField(blank=True, null=True) # computed 

    def __unicode__(self):
        return u'%s / %s' % (self.jobseeker, self.mentor)

    def is_active(self):
        return not self.has_expired()

    def has_expired(self):
        return datetime.date.today() > self.expirationDate
    
    def set_expiration(self):
        duration = 5  # in months 
        y = self.startDate.year
        m = self.startDate.month + duration
        d = self.startDate.day 
        if (m > 12):
            m = m % 12 
            y += 1 
        expiration = datetime.date(y, m, 1)
        # check if the start month has more days then the expiration month
        (dontcare, daysInThisMonth) = calendar.monthrange(y,m)
        if d >= daysInThisMonth:
            d = daysInThisMonth
        self.expirationDate = expiration + datetime.timedelta(d-1)

    class Meta:
        ordering = ['-startDate'];

class Company(models.Model):
    name = models.CharField(_('Name'), max_length=32)
    division = models.CharField(_('Division'), max_length=64,blank=True,null=True)
    address = models.CharField(_('Address'), max_length=128)
    city = models.CharField(_('City'), max_length=32)
    state_province = models.CharField(_('State or Province'),max_length=32)
    country = models.CharField(_('Country'),max_length=3)   # select from three digit country code. 
    zipCode = models.CharField(_('Zip'),max_length=16, blank=True, null=True)
    website = models.URLField(_('Website'))
    comment = models.CharField(_('Comment'), max_length=256,blank=True,null=True)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name'];

"""
People a job seeker has met along the way. 
"""
class Person(models.Model):
    first_name = models.CharField(_('First name'),max_length=16)
    last_name = models.CharField(_('Last name'),max_length=16)
    title = models.CharField(_('Title'),max_length=64)
    company = models.ForeignKey(Company, unique=True, blank=True, null=True)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return u'%s %s' % (self.first_name , self.last_name)

class Position(models.Model):
    company = models.ForeignKey(Company, unique=True)
    title = models.CharField(max_length=64)
    website = models.URLField()
    comment = models.CharField(max_length=256,blank=True,null=True)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return  u'%s at %s' % (self.title, self.company)

    class Meta:
        ordering = ['title']

"""
The job seeker can record activities. When is the interview? 
Apply for a job? Sent thank to interviewer? 
"""
class Activity(models.Model):
    when = models.DateField()
    time = models.TimeField()
    comment = models.CharField(max_length=256,blank=True,null=True)
    user = models.ForeignKey(UserProfile)

    """
    Since Activity is abstract, there is no manager object (ie, objects). 
    However we want a complete list of all activities.
    """
    @staticmethod
    def getAll(profile_id):
        rc = []
        rc.extend(Interview.objects.filter(user=profile_id))
        rc.extend(Apply.objects.filter(user=profile_id))
        rc.extend(Networking.objects.filter(user=profile_id))
        rc.extend(Conversation.objects.filter(user=profile_id))
        rc.extend(MentorMeeting.objects.filter(user=profile_id))
        rc.extend(Lunch.objects.filter(user=profile_id))
        rc.reverse()
        return rc

    class Meta:
        abstract = True
        ordering = ['-when','time']

'''
NB:  You may notice that the tag field is not used in the python code. 
It is used to compose the REST calls for editing and deleting 
activities in the template code.
'''

class Interview(Activity):
    position = models.ForeignKey(Position, unique=True)
    withWhom = models.ForeignKey(Person)

    tag = "interview"

    def __unicode__(self):
        return  u'Interview with %s %s at %s for %s' % (self.withWhom.first_name, self.withWhom.last_name, self.position.company.name, self.position.title)

"""
applied for job
"""
class Apply(Activity): 
    position = models.ForeignKey(Position, unique=True)

    tag = "apply"

    def __unicode__(self):
        return  u'Applied for %s at %s' % (self.position.title, self.position.company.name)

"""
networking at professional event. Company.name is the venue.
""" 
class Networking(Activity):
    venue = models.ForeignKey(Company, unique=True)

    tag = "networking"

    def __unicode__(self):
        return  u'Networking at %s' % (self.venue.name)

"""
Lunch with colleague 
"""
class Lunch (Activity):
    withWhom = models.ForeignKey(Person)
    venue = models.CharField(max_length=128,blank=True,null=True)

    tag = "lunch"
    
    def __unicode__(self):
        return u'Lunch(or coffee) with %s %s at %s' % (self.withWhom.first_name, self.withWhom.last_name, self.venue)

"""
Meet with Mentor. Assumption: The Mentorship should have been  
"""
class MentorMeeting(Activity):
    mentorship = models.ForeignKey(Mentorship, unique=True)
    face_to_face = models.BooleanField(default=False)

    tag = "mentormeeting"

    def __unicode__(self):
        return  u'Met with %s' % (self.mentorship.mentor)

"""
Conversation can be via email, phone, in-person, etc.
"""
class Conversation(Activity):
    METHOD_OF_COMMUNICATION = (
        ("email","E-mail"),
        ("phone","Phone"),
        ("faceToFace","face to face"),
    )
    via = models.CharField(max_length=16, choices=METHOD_OF_COMMUNICATION)
    person = models.ForeignKey(Person, unique=True) 
    
    tag = "conversation"

    def __unicode__(self):
        return  u'Spoke with %s %s via %s' % (self.person.first_name, self.person.last_name ,self.via)

"""
This models simply stores an elevator pitch. 
"""
class Pitch(models.Model):
    role = models.CharField(_('Role'), max_length=32)
    thePitch = models.CharField(_('Pitch'), max_length=256)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.thePitch
    

"""
Other websites are useful for the job hunt. Everyone has an online 
resume, linkedin profile or similar. You might also want to highlight
your twitter feed. Software developers might have a github profile. 
"""
class OnlinePresence(models.Model):
    name = models.CharField(_('website name'), max_length=32)
    url = models.URLField(_('URL'), blank=True) 
    user = models.ForeignKey(UserProfile)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

"""
Behaviorial questions and results to them in PAR format. 
"""
class PAR(models.Model):
    question = models.CharField(_('Question'), max_length=128)
    par_response = models.TextField(_('Response')) 
    user = models.ForeignKey(UserProfile)
    
    class Meta:
        ordering = ['question']
