from django.utils import unittest

import datetime

from django.contrib.auth.models import User
from .models import UserProfile, Mentorship, may_access_control


def create_a_user(dict):
    user = User.objects.create_user(
        username=dict['username'],
        email=dict['email'],
        password=dict['password'])
    user.save()
    profile = user.get_profile()
    profile.title = dict['title']
    profile.is_upglo_staff = dict['is_upglo']
    profile.save()
    return user.id, profile


class ValidateModels(unittest.TestCase):
    mentorship = None
    # cast
    emily = "Emily"  # upglo staff
    emilyId = None
    yohannes = "Yohannes"  # jobseeker
    yohannesId = None
    diego = "Diego"  # Yohannes' mentor
    diegoId = None
    elena = "Elena"  # unrelated job seeker
    elenaId = None
    jose = "Jose"  # unrelated mentor
    joseId = None

    def setUp(self):
        '''
        populate the database
        '''
        self.emilyId, coordinator_profile = create_a_user(
            {'username': self.emily,
             'email': self.emily + "@gmail.com",
             'password': "secret",
             'is_upglo': True,
             'role': "coordinator",
             'title': "UpGlo Coordinator"})
        self.yohannesId, jobseeker_profile = create_a_user(
            {'username': self.yohannes,
             'email': self.yohannes + "@gmail.com",
             'password': "secret",
             'is_upglo': False,
             'role': "jobseeker",
             'title': "Research Assoicate "})
        self.diegoId, mentor_profile = create_a_user(
            {'username': self.diego,
             'email': self.diego + "@gmail.com",
             'password': "secret",
             'is_upglo': False,
             'role': "mentor",
             'title': "Human Resources"})
        # establish a mentorship
        self.mentorship = Mentorship(jobseeker=jobseeker_profile,
                                     mentor=mentor_profile,
                                     startDate=datetime.date.today())
        self.mentorship.set_expiration()
        self.mentorship.save()
        self.elenaId, dontcare = create_a_user(
            {'username': self.elena,
             'email': self.elena + "@gmail.com",
             'password': "secret",
             'is_upglo': False,
             'role': "jobseeker",
             'title': "Research Assoicate "})
        self.joseId, dontcare = create_a_user(
            {'username': self.jose,
             'email': self.jose + "@gmail.com",
             'password': "secret",
             'is_upglo': False,
             'role': "mentor",
             'title': "Human Resources"})

    def test_mentorship(self):
        # Is the mentorship active?
        self.assertTrue(self.mentorship.is_active())
        #  Can the mentor access their mentee?
        self.assertTrue(may_access_control(self.diegoId, self.yohannesId))
        #  Ensure an unrelated job seeker can't see profile?
        self.assertFalse(
            may_access_control(self.elenaId, self.yohannesId))
        # Ensure unrelated mentor can't see profile?
        self.assertFalse(
            may_access_control(self.joseId, self.yohannesId))
        # Ensure UpGlo staff can access jobseeker.
        self.assertTrue(
            may_access_control(self.emilyId, self.yohannesId))
