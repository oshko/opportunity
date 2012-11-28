from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class Company(models.Model):
    name = models.CharField(_('Name'), max_length=32)
    address = models.CharField(_('Address'), max_length=128)
    city = models.CharField(_('City'), max_length=32)
    state_province = models.CharField(_('State or Province'),max_length=32)
    country = models.CharField(_('Country'),max_length=3)   # select from three digit country code. 
    website = models.URLField(_('Website'))

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
    company = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return self.name

class Position(models.Model):
    company = models.ForeignKey(Company, unique=True)
    title = models.CharField(max_length=64)
    website = models.URLField()
    comment = models.CharField(max_length=256)

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
    comment = models.CharField(max_length=256)

    class Meta:
        abstract = True
        ordering = ['when']

class Interview(Activity):
    position = models.ForeignKey(Position, unique=True)
    company = models.ForeignKey(Company, unique=True)
    withWhom = models.ManyToManyField(Person)

    def __unicode__(self):
        return  u'interviewing with %s for %s' % (self.company.name, self.Position.title)

class Apply(Activity): 
    '''
    applied for job
    '''
    position = models.ForeignKey(Position, unique=True)
    company = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return  u'Applied for %s at %s' % (self.Position.title, self.company.name)
 
class Networking(Activity):
    '''
    networking at professional event. Company.name is the venue.
    '''
    venue = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return  u'Networking at %s' % (self.company.name)

class Gratitude(Activity):
    '''
    send thank you letters.
    '''
    person = models.ForeignKey(Person, unique=True)

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

    def __unicode__(self):
        return  u'Spoke %s via ' % (self.person.name,self.via)

class UserProfile(models.Model):
    """
    A UserProfile is a person which uses our system.
    """
    user = models.OneToOneField(User)
    title = models.CharField(max_length=32) 
    #pitch = models.CharField(max_length=128)

    def __unicode__(self):
        return self.user.username

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
    question = models.CharField(_('question'), max_length=128)
    problem = models.CharField(_('problem'), max_length=256)
    action = models.CharField(_('action'), max_length=256)
    result = models.CharField(_('result'), max_length=256)
    user = models.ForeignKey(UserProfile)

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

