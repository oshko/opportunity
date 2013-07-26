from django.utils import unittest

import datetime

from django.contrib.auth.models import User
from .models import Company, UserProfile, Mentorship
from .views import populateCompany
from .access import may_access_control


class FetchFromCrunch(unittest.TestCase):
    def test_normal(self):
        '''
        The simpliest case is a single token with no special characters
        which matches a specific company in crunchbase.
        '''
        co = Company()
        co.name = "Solum"
        populateCompany(co)
        self.assertEqual(co.city, "Mountain View")

    def test_encoding(self):
        '''
        What happens if the string needs to be encode?
        '''
        co = Company()
        co.name = "Red Hat"
        populateCompany(co)
        self.assertEqual(co.city, "Raleigh")

    def test_matches_multiple(self):
        '''
        What happens if a company has multiple offices?
        '''
        co = Company()
        co.name = "IBM"
        populateCompany(co)
        self.assertEqual(co.city, "Armonk")

    def test_no_match(self):
        '''
        What happens if there is no match with crunchbase?
        '''
        co = Company()
        name = "pirulito"
        co.name = name
        populateCompany(co)
        self.assertEqual(co.name, name)
        self.assertEqual(co.city, "")


def create_a_user_for_test(aDict):
    user = User.objects.create_user(
        username=aDict['username'],
        email=aDict['email'],
        password=aDict['password'])
    user.save()
    profile = user.get_profile()
    profile.title = aDict['title']
    profile.is_upglo_staff = aDict['is_upglo']
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
        self.emilyId, coordinator_profile = create_a_user_for_test(
            {'username': self.emily,
             'email': self.emily + "@gmail.com",
             'password': "secret",
             'is_upglo': True,
             'role': "coordinator",
             'title': "UpGlo Coordinator"})
        self.yohannesId, jobseeker_profile = create_a_user_for_test(
            {'username': self.yohannes,
             'email': self.yohannes + "@gmail.com",
             'password': "secret",
             'is_upglo': False,
             'role': "jobseeker",
             'title': "Research Assoicate "})
        self.diegoId, mentor_profile = create_a_user_for_test(
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
        self.elenaId, dontcare = create_a_user_for_test(
            {'username': self.elena,
             'email': self.elena + "@gmail.com",
             'password': "secret",
             'is_upglo': False,
             'role': "jobseeker",
             'title': "Research Assoicate "})
        self.joseId, dontcare = create_a_user_for_test(
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
