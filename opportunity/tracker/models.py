from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=32)
    state_province = models.CharField(max_length=32)
    country = models.CharField(max_length=3)   # select from three digit country code. 
    website = models.URLField()

    def __unicode__(self):
        return self.name


# A JobSeekerProfile is a person which uses our system. 
# see http://www.turnkeylinux.org/blog/django-profile
# 
class JobSeekerProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField("Website", blank=True)
    company = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return self.user

# People a job seeker has met along the way. 
class Person(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    company = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return self.name

class Position(models.Model):
    company = models.ForeignKey(Company, unique=True)
    title = models.CharField(max_length=64)
    website = models.URLField()

    def __unicode__(self):
        return  u'%s at %s' % (self.title, self.company)

# The job seeker can record activities. When is the interview? 
# Apply for a job? Sent thank to interviewer? 
class Activity(models.Model):
    when = models.DateField()
    comment = models.CharField(max_length=256)

    class Meta:
        abstract = True

# job interview 
class Interview(Activity):
    position = models.ForeignKey(Position, unique=True)
    company = models.ForeignKey(Company, unique=True)
    withWhom = models.ManyToManyField(Person)

    def __unicode__(self):
        return  u'interviewing with %s for %s' % (self.company.name, self.Position.title)

# applied for job
class Apply(Activity): 
    position = models.ForeignKey(Position, unique=True)
    company = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return  u'Applied for %s at %s' % (self.Position.title, self.company.name)

# networking at professional event. Company.name is the venue. 
class Networking(Activity):
    venue = models.ForeignKey(Company, unique=True)

    def __unicode__(self):
        return  u'Networking at %s' % (self.company.name)

# sent thank you letters. 
class Gratitude(Activity):
    person = models.ForeignKey(Person, unique=True)

    def __unicode__(self):
        return  u'Thank %s' % (self.person.name)

# Conversation can be via email, phone, in-person, etc.
class Conversation(Activity):
    METHOD_OF_COMMUNICATION = (
        ("email","E-mail"),
        ("phone","Phone"),
        ("faceToFace","face to face"),
    )
    via = models.CharField(max_length=16, choices=METHOD_OF_COMMUNICATION)
    person = models.ForeignKey(Person, unique=True) 

    def __unicode__(self):
        return  u'Spoke %s via ' % (self.person.name,self.via)

