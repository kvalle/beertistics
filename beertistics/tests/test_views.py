import unittest
from beertistics.tests.base import BeertisticsTestCase

class EditNoteTests(unittest.TestCase, BeertisticsTestCase):

    def setUp(self):
        self.commonSetUp()
        self.login()
        
    def test_frontpage(self):
        response = self.app.get('/')
        assert "<h1>TODO" in response.data

    def test_settings(self):
        response = self.app.get('/settings')
        assert "<h1>TODO: settings</h1>" in response.data
    
if __name__ == '__main__':
    unittest.main()
