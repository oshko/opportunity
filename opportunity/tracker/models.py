from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
    """
    A UserProfile is a person which uses our system.
    """
    user = models.OneToOneField(User)
    title = models.CharField(max_length=32) 

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

class Person(models.Model):
    '''
    People a job seeker has met along the way. 
    '''
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

class Activity(models.Model):
    '''
    The job seeker can record activities. When is the interview? 
	Apply for a job? Sent thank to interviewer? 
    '''
    when = models.DateField()
    time = models.TimeField()
    comment = models.CharField(max_length=256,blank=True,null=True)
    user = models.ForeignKey(UserProfile)

    '''
    Since Activity is abstract, there is no manager object (ie, objects). 
    However we want a complete list of all activities.
    '''
    @staticmethod
    def getAll():
        rc = []
        rc.extend(Interview.objects.all())
        rc.extend(Apply.objects.all())
        rc.extend(Networking.objects.all())
        rc.extend(Gratitude.objects.all())
        rc.extend(Conversation.objects.all())
        return rc

    class Meta:
        abstract = True
        ordering = ['when']

class Interview(Activity):
    position = models.ForeignKey(Position, unique=True)
    withWhom = models.ForeignKey(Person)
    
    tag = "interview"

    def __unicode__(self):
        return  u'Interview with %s %s at %s for %s' % (self.withWhom.first_name, self.withWhom.last_name, self.position.company.name, self.position.title)

class Apply(Activity): 
    '''
    applied for job
    '''
    position = models.ForeignKey(Position, unique=True)

    tag = "apply"

    def __unicode__(self):
        return  u'Applied for %s at %s' % (self.position.title, self.position.company.name)
 
class Networking(Activity):
    '''
    networking at professional event. Company.name is the venue.
    '''
    venue = models.ForeignKey(Company, unique=True)

    tag = "networking"

    def __unicode__(self):
        return  u'Networking at %s' % (self.venue.name)

class Lunch (Activity):
    '''
    Lunch with colleague 
    '''
    withWhom = models.ForeignKey(Person)
    venue = models.CharField(max_length=128,blank=True,null=True)
    tag = "lunch"
    
    def __unicode__(self):
        return u'Lunch with %s %s at %s' % (self.withWhom.first_name, self.withWhom.last_name, self.venue)

class Gratitude(Activity):
    '''
    send thank you letters.
    '''
    person = models.ForeignKey(Person, unique=True)

    tag = "gratitude"

    def __unicode__(self):
        return  u'Thank %s' % (self.person.name)

class Conversation(Activity):
    '''
    Conversation can be via email, phone, in-person, etc.
    '''
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



class Pitch(models.Model):
    """
    This models simply stores an elevator pitch. 
    """
    role = models.CharField(_('Role'), max_length=32)
    thePitch = models.CharField(_('Pitch'), max_length=256)
    user = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.thePitch
    

class OnlinePresence(models.Model):
    """
    Other websites are useful for the job hunt. Everyone has an online 
    resume, linkedin profile or similar. You might also want to highlight
    your twitter feed. Software developers might have a github profile. 
    """
    name = models.CharField(_('website name'), max_length=32)
    url = models.URLField(_('URL'), blank=True) 
    user = models.ForeignKey(UserProfile)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class PAR(models.Model):
    """
    Behaviorial questions and results to them in PAR format. 
    """
    question = models.CharField(_('Question'), max_length=128)
    par_response = models.TextField(_('Response')) 
    user = models.ForeignKey(UserProfile)
    
    class Meta:
        ordering = ['question']


