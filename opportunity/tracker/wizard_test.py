import unittest
from .wizard import *


class InterviewTest(unittest.TestCase):

    def test_interview_seq(self):
        '''
        The wizards job is to define the sequence of views and
        associated arguments used to record information about
        an interview
        '''
        mock_session = {}
        obj = Composite.factory(INTERVIEW, NEW_ACTIVITY)
        # user selected interview from dashboard
        self.assertEqual(obj.get_next_url(),
            '/prospect/add?activity=interview')

        obj = Composite.factory(INTERVIEW, COMPANY)
        obj.set(mock_session, CO_ID, 3)
        self.assertEqual(obj.get_next_url(),
                         '/position/add?activity=interview&co_id=3')

        obj = Composite.factory(INTERVIEW, POSITION)
        obj.set(mock_session, POS_ID, 4)
        self.assertEqual(obj.get_next_url(),
                         '/contact/add?activity=interview&co_id=3&pos_id=4')

        obj = Composite.factory(INTERVIEW, CONTACT)
        obj.set(mock_session, PER_ID, 5)
        self.assertEqual(obj.get_next_url(),
                         '/interview/add?activity=interview&co_id=3&per_id=5&pos_id=4')

        obj = Composite.factory(INTERVIEW, INTERVIEW)
        self.assertEqual(obj.get_next_url(),
                         '/dashboard/')


class ApplyTest(unittest.TestCase):

    def test_apply_seq(self):
        '''
        The wizards job is to define the sequence of views and
        associated arguments used to record information about
        applying for a specfic position.
        '''
        mock_session = {}
        obj = Composite.factory(APPLY, NEW_ACTIVITY)
        # user selected interview from dashboard
        self.assertEqual(obj.get_next_url(),
            '/prospect/add?activity=apply')

        obj = Composite.factory(APPLY, COMPANY)
        obj.set(mock_session, CO_ID, 3)
        self.assertEqual(obj.get_next_url(),
            '/position/add?activity=apply&co_id=3')

        obj = Composite.factory(APPLY, POSITION)
        obj.set(mock_session, POS_ID, 4)
        self.assertEqual(obj.get_next_url(),
            '/apply/add?activity=apply&co_id=3&pos_id=4')

        obj = Composite.factory(APPLY, APPLY)
        self.assertEqual(obj.get_next_url(),
            '/dashboard/')


class ConversationText(unittest.TestCase):

    def test_conversation_seq(self):
        '''
        The wizards job is to define the sequence of views and
        associated arguments used to record information about
        a conversation you had along the way.
        '''
        mock_session = {}
        obj = Composite.factory(CONVERSATION, NEW_ACTIVITY)
        # user selected interview from dashboard
        self.assertEqual(obj.get_next_url(),
            '/contact/add?activity=conversation')

        obj = Composite.factory(CONVERSATION, CONTACT)
        obj.set(mock_session, PER_ID, 4)
        self.assertEqual(obj.get_next_url(),
            '/conversation/add?activity=conversation&per_id=4')

        obj = Composite.factory(CONVERSATION, CONVERSATION)
        self.assertEqual(obj.get_next_url(),
            '/dashboard/')


class NetworkingTest(unittest.TestCase):
    def test_networking_seq(self):
        '''
        The wizards job is to define the sequence of views and
        associated arguments used to record information about
        a networking events.
        '''
        mock_session = {}
        obj = Composite.factory(NETWORKING, NEW_ACTIVITY)
        # user selected interview from dashboard
        self.assertEqual(obj.get_next_url(),
            '/prospect/add?activity=networking')

        obj = Composite.factory(NETWORKING, COMPANY)
        obj.set(mock_session, CO_ID, 3)
        self.assertEqual(obj.get_next_url(),
            '/networking/add?activity=networking&co_id=3')

        obj = Composite.factory(NETWORKING, NETWORKING)
        self.assertEqual(obj.get_next_url(),
            '/dashboard/')


if __name__ == '__main__':
    unittest.main()
