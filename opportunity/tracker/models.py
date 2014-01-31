from __future__ import unicode_literals
import calendar
import datetime
import logging

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import six

logger = logging.getLogger(__name__)


def secret_society(user_profile, veiwing_profile_id):
    '''
    Given the UserProfile for the current user, compute a list of
    UserProfiles which are either mentors to and job seekers supported
    by this user.

    viewing_profile_id used to determine which page is being viewed and set
    the selectors default.
    '''
    ret = [('self', user_profile.id,
            True if user_profile.id == veiwing_profile_id else False)]
    # Retrieves all mentorships in which the current user is either
    # a jobseeker or mentor?
    m_list = Mentorship.objects.filter(
        Q(jobseeker=user_profile) | Q(mentor=user_profile))

    for m in m_list:
        if m.jobseeker != user_profile:
            ret.append((m.jobseeker.user.first_name.strip()
                        + ' ' + m.jobseeker.user.last_name.strip(),
                        m.jobseeker.id,
                        True if m.jobseeker.id == veiwing_profile_id else False))
        else:
            ret.append((m.mentor.user.first_name.strip()
                        + ' ' + m.mentor.user.last_name.strip(),
                        m.mentor.id,
                        True if m.mentor.id == veiwing_profile_id else False))
    return ret


def perm_and_params(requester, target_id):
    '''
    Given a UserProfile and a target uid, return a dict which contains
    permission and parameters with respect to whether the requestion
    can view the page.

    'perm_p' - boolean - can requester view this page?
    'page_owner_p' - boolean - Who owns the page ?
    'page_owner_name' - What is the name of the page owner?
    'profile_id' - What is the uid of the content to display?
    'warning_message' - Warning message to display if any ?
    '''
    page_options = {}
    page_options['perm_p'] = False
    page_options['page_owner_p'] = False
    page_options['page_owner_name'] = 'Unauthorized'
    page_options['profile_id'] = -1
    page_options['warning_message'] = None

    if target_id:
        # request to view someone elses page
        # perm_p is false by default. So, no need for else block

        if target_id and may_access_control(requester.id,
                                            target_id):
            if target_id == requester.id:
                page_options['profile_id'] = requester.id
                page_options['page_owner_p'] = True
                page_options['page_owner_name'] = 'My'
                page_options['perm_p'] = True
            else:
                page_options['profile_id'] = target_id
                mentee = UserProfile.objects.get(pk=target_id)
                page_options['page_owner_name'] = mentee.user.username.strip() + "'s"
                page_options['perm_p'] = True
    else:
        # no target id - what's the right default?
        # perm_p is false by default. Coordinator should always
        # be associated mentee id. if not, the default generates an error.
        if requester.is_job_seeker():
                page_options['profile_id'] = requester.id
                page_options['page_owner_p'] = True
                page_options['page_owner_name'] = 'My'
                page_options['perm_p'] = True
        elif requester.is_mentor():
            mentee_id, err_message = requester.has_mentee()
            if mentee_id and may_access_control(requester.id, mentee_id):
                page_options['profile_id'] = mentee_id
                mentee = UserProfile.objects.get(pk=mentee_id)
                page_options['page_owner_name'] = mentee.user.username.strip() + "'s"
                page_options['perm_p'] = True
            else:
                # mentor is logged in but has no mentee.
                page_options['profile_id'] = requester.id
                page_options['page_owner_p'] = True
                page_options['page_owner_name'] = 'My'
                page_options['perm_p'] = True
                warning_message = 'No mentee assigned, yet.'
    return page_options


def may_access_control(requester_id, target_id):
    '''
    can user with requester_id access a page for target_id?

    requester_id - is user profile id who wants access
    target_id - is user profile id owns the data.

    '''
    ret = False
    # urls pass ints as strings. What if someone forgets to convert them?
    if not (isinstance(requester_id, int) and isinstance(target_id, int)):
        logger.error('mentor ids must be ints')
        return False
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
            (Q(jobseeker=requester_id) & Q(mentor=target_id)) |
            (Q(jobseeker=target_id) & Q(mentor=requester_id)))
        if len(m_rel) == 1:
            ret = True
    return ret


@python_2_unicode_compatible
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

    def __str__(self):
        return self.user.username

    def is_coordinator(self):
        '''
        Is a coordinator?
        '''
        return self.role == self.COORDINATOR

    def is_job_seeker(self):
        '''
        is a job seeker?
        '''
        return self.role == self.JOB_SEEKER

    def is_mentor(self):
        '''
        Is a mentor?
        '''
        return self.role == self.MENTOR

    def is_mentor_of(self, js_id):
        '''
        Is this user the mentor of id?
        '''
        if js_id:
            rc = True if may_access_control(self.id, js_id) else False
        else:
            rc = False
        return rc

    def has_mentee(self):
        '''
        Has this user been assigned to work with a job seeker?
        Given a user id return job seek id of mentee if any, else None
        '''
        rc = None
        err_msg = None
        if self.is_mentor():
            m_rel = Mentorship.objects.filter(mentor__id=self.id)
            if len(m_rel) >= 1:
                rc = m_rel[0].jobseeker_id
            else:
                err_msg = 'No mentee has been assigned, yet.'
        else:
            err_msg = 'You must be a mentor to view this page'
        return rc, err_msg

    def get_mentorship(self):
        '''
        Given user id return mentorship or None if there isn't one.
        '''
        rc = None
        if self.is_job_seeker():
            rc = Mentorship.objects.filter(jobseeker__id=self.id)
            if len(rc) >= 1:
                rc = rc[0]
        return rc


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


@python_2_unicode_compatible
class Mentorship(models.Model):
    '''
    A mentor assists a mentee with respect to finding a job.
    UpGlo Mentorships last five months.
    '''
    jobseeker = models.ForeignKey(UserProfile, related_name='jobseeker')
    mentor = models.ForeignKey(UserProfile, related_name='mentor')
    startDate = models.DateField()  # should be set in UI
    expirationDate = models.DateField(blank=True, null=True)  # computed

    def __str__(self):
        return '%s / %s' % (self.jobseeker, self.mentor)

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
        (dontcare, daysInThisMonth) = calendar.monthrange(y, m)
        if d >= daysInThisMonth:
            d = daysInThisMonth
        self.expirationDate = expiration + datetime.timedelta(d - 1)

    class Meta:
        ordering = ['-startDate']


@python_2_unicode_compatible
class Company(models.Model):
    name = models.CharField(_('Name'), max_length=32)
    division = models.CharField(_('Division'),
                                max_length=64,
                                blank=True, null=True)
    address = models.CharField(_('Address'), max_length=128)
    city = models.CharField(_('City'), max_length=32)
    state_province = models.CharField(_('State or Province'), max_length=32)
    country = models.CharField(
        _('Country'),
        max_length=3)   # select from three digit country code.
    zipCode = models.CharField(
        _('Zip'), max_length=16, blank=True, null=True)
    website = models.URLField(_('Website'))
    user = models.ForeignKey(UserProfile)
    # is this company a prospective employer or simply a networking venue?
    is_prospective = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ['name']


@python_2_unicode_compatible
class Person(models.Model):
    """
    People a job seeker has met along the way.
    """
    first_name = models.CharField(_('First name'), max_length=16)
    last_name = models.CharField(_('Last name'), max_length=16)
    title = models.CharField(_('Title'), max_length=64)
    company = models.ForeignKey(Company, unique=True, blank=True, null=True)
    user = models.ForeignKey(UserProfile)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


@python_2_unicode_compatible
class Position(models.Model):
    company = models.ForeignKey(Company)
    title = models.CharField(max_length=64)
    website = models.URLField()
    user = models.ForeignKey(UserProfile)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s at %s' % (self.title, self.company)

    class Meta:
        ordering = ['title']


@python_2_unicode_compatible
class Activity(models.Model):
    """
    The job seeker can record activities. When is the interview?
    Apply for a job? Sent thank to interviewer?
    """
    when = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(UserProfile)

    def __str__(self):
        return 'generic activity '

    @staticmethod
    def getAll(profile_id):
        """
        Since Activity is abstract, there is no manager object (ie, objects).
        However we want a complete list of all activities.
        """
        rc = []
        rc.extend(Interview.objects.filter(user=profile_id))
        rc.extend(Apply.objects.filter(user=profile_id))
        rc.extend(Networking.objects.filter(user=profile_id))
        rc.extend(Conversation.objects.filter(user=profile_id))
        rc.extend(MentorMeeting.objects.filter(user=profile_id))
        rc.extend(Lunch.objects.filter(user=profile_id))
        rc = sorted(rc, key=lambda act: act.time, reverse=True)  # 2nd - time
        rc = sorted(rc, key=lambda act: act.when, reverse=True)  # primary - date
        return rc

    class Meta:
        abstract = True

'''
NB:  You may notice that the tag field is not used in the python code.
It is used to compose the REST calls for editing and deleting
activities in the template code.
'''


@python_2_unicode_compatible
class Interview(Activity):
    position = models.ForeignKey(Position, unique=True)
    withWhom = models.ForeignKey(Person)

    tag = "interview"

    def __str__(self):
        return 'Interview with %s %s at %s for %s' % (
            self.withWhom.first_name, self.withWhom.last_name,
            self.position.company.name, self.position.title)


@python_2_unicode_compatible
class Apply(Activity):
    """
    applied for job
    """
    position = models.ForeignKey(Position, unique=True)

    tag = "apply"

    def __str__(self):
        return 'Applied for %s at %s' % (
            self.position.title, self.position.company.name)


@python_2_unicode_compatible
class Networking(Activity):
    """
    networking at professional event. Company.name is the venue.
    """
    venue = models.ForeignKey(Company, unique=True)

    tag = "networking"

    def __str__(self):
        return 'Networking at %s' % (self.venue.name)


@python_2_unicode_compatible
class Lunch (Activity):
    """
    Lunch with colleague
    """
    withWhom = models.ForeignKey(Person)
    venue = models.CharField(max_length=128, blank=True, null=True)

    tag = "lunch"

    def __str__(self):
        return 'Lunch(or coffee) with %s %s at %s' % (
            self.withWhom.first_name, self.withWhom.last_name, self.venue)


@python_2_unicode_compatible
class MentorMeeting(Activity):
    """
    Meet with Mentor.
    """
    mentorship = models.ForeignKey(Mentorship, unique=True)
    face_to_face = models.BooleanField(default=False)

    tag = "mentormeeting"

    @staticmethod
    def factory(user, mentorship):
        rc = MentorMeeting()
        rc.user = user
        rc.mentorship = mentorship
        return rc

    def __str__(self):
        return 'Met with %s' % (self.mentorship.mentor)


@python_2_unicode_compatible
class Conversation(Activity):
    """
    Conversation can be via email, phone, in-person, etc.
    """
    METHOD_OF_COMMUNICATION = (
        ("email", "E-mail"),
        ("phone", "Phone"),
        ("faceToFace", "face to face"),
    )
    via = models.CharField(max_length=16, choices=METHOD_OF_COMMUNICATION)
    person = models.ForeignKey(Person, unique=True)

    tag = "conversation"

    def __str__(self):
        msg = 'Spoke with {0} {1} '.format(
            self.person.first_name, self.person.last_name)
        if self.via == "faceToFace":
            msg += " in person"
        else:
            msg += " via {0}".format(METHOD_OF_COMMUNICATION[self.via])
        return msg


@python_2_unicode_compatible
class Pitch(models.Model):
    """
    This Models Simply Stores An Elevator Pitch.
    """
    role = models.CharField(_('Role'), max_length=32)
    thePitch = models.CharField(_('Pitch'), max_length=256)
    user = models.ForeignKey(UserProfile)

    def __str__(self):
        return self.thePitch


@python_2_unicode_compatible
class OnlinePresence(models.Model):
    """
    Other websites are useful for the job hunt. Everyone has an online
    resume, linkedin profile or similar. You might also want to highlight
    your twitter feed. Software developers might have a github profile.
    """
    name = models.CharField(_('website name'), max_length=32)
    url = models.URLField(_('URL'), blank=True)
    user = models.ForeignKey(UserProfile)

    def __str__(self):
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


class TimeStampedModel(models.Model):
    '''
    The book Two Scoops recommends creating a ABC for time stamps.
    '''
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Comment(TimeStampedModel):
    author = models.ForeignKey(UserProfile)
    comment = models.CharField(_('Comment'), max_length=1024)

    class Meta:
        abstract = True


class PositionComment(Comment):
    position = models.ForeignKey(Position)


class CompanyComment(Comment):
    company = models.ForeignKey(Company)


class InterviewComment(Comment):
    activity = models.ForeignKey(Interview)


class ApplyComment(Comment):
    activity = models.ForeignKey(Apply)


class NetworkingComment(Comment):
    activity = models.ForeignKey(Networking)


class LunchComment(Comment):
    activity = models.ForeignKey(Lunch)


class MentorMeetingComment(Comment):
    activity = models.ForeignKey(MentorMeeting)


class ConversationComment(Comment):
    activity = models.ForeignKey(Conversation)
