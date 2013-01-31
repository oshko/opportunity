from django.utils import unittest

from models import Company
from views import populateCompany

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
        If there is a space in the given name, you need to encode the
        string. If you fail to so, you'll likely 
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
        co.name = "pirulito" 
        populateCompany(co)
        self.assertEqual(co.name, name)
        self.assertEqual(co.city, "")
