import unittest
from .wizard import *

class InterviewTest(unittest.TestCase):

    def test_interview_new(self):
        '''
        The wizards job is to define the sequence of views and
        associated arguments. 
        '''
        mock_session = {} 
        obj = Composite.factory(INTERVIEW, NEW_ACTIVITY)
        # user selected interview from dashboard
        self.assertEqual(obj.get_url(),
            '/prospect/add?activity=interview')

        obj = Composite.factory(INTERVIEW, COMPANY)
        obj.set(mock_session, CO_ID, 3)
        self.assertEqual(obj.get_url(),
            '/position/add?activity=interview&co_id=3')

        mock_session = {CO_ID: 3}
        obj = Composite.factory(INTERVIEW, POSITION)
        obj.set(mock_session, POS_ID, 4)
        self.assertEqual(obj.get_url(),
            '/contact/add?activity=interview&co_id=3&pos_id=4')


if __name__ == '__main__':
    unittest.main()
