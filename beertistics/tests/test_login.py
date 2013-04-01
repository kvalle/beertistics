import unittest
from beertistics.tests.base import BeertisticsTestCase

class LoginTests(unittest.TestCase, BeertisticsTestCase):

    def setUp(self):
        self.commonSetUp()

    def test_login_required(self):
        response = self.app.get('/', follow_redirects=True)
        assert '<h1>Log in</h1>' in response.data
        
    def test_login_works(self):
        self.login()
        response = self.app.get('/')
        assert 'Log out' in response.data
        
    def test_login_bad_username(self):
        response = self.login(user="invalid user")
        assert "Invalid username or password." in response.data

    def test_login_bad_password(self):
        response = self.login(password="invalid pwd")
        assert "Invalid username or password." in response.data

    def test_login_redirects_properly(self):
        response = self.app.get('/settings', follow_redirects=True)
        assert "You must log in" in response.data

        response = self.login()
        assert response.status_code == 302
        assert response.location.endswith("settings")
        
    def test_logout(self):
        self.login()
        response = self.app.get('/log-out', follow_redirects=True)
        assert "You were logged out" in response.data
        response = self.app.get('/', follow_redirects=True)
        assert "You must log in" in response.data

if __name__ == '__main__':
    unittest.main()
