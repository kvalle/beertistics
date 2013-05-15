import unittest
from beertistics import app
from beertistics.tests.base import BeertisticsTestCase


class LoginWithStubTests(unittest.TestCase, BeertisticsTestCase):
    """
    Unit tests for all parts of the login other than the Untappd OAuth itself.
    """

    def setUp(self):
        self.commonSetUp()

    def test_login_required_for_frontpage_if_not_yet_logged_in(self):
        response = self.app.get('/', follow_redirects=True)
        assert 'log in' in response.data

    def test_login_page_redirects_end_up_at_root(self):
        response = self.app.get('/log-in', follow_redirects=True)
        assert '<title>Overview' in response.data

    def test_other_pages_redirect_correctly_after_login(self):
        response = self.get_with_redirect('/visual/punchcard')
        assert '<div id="punchcard">' in response.data

    def test_logout_works_and_redirects_to_login_page(self):
        self.login()
        response = self.app.get('/', follow_redirects=True)
        assert "Log out" in response.data

        response = self.app.get('/log-out', follow_redirects=True)
        assert "You were logged out" in response.data
        assert "log in" in response.data

    def test_login_reuired_for_all_api_pages(self):
        pages = [str(rule) for rule in app.url_map.iter_rules()
                    if str(rule).startswith("/api")]
        for page in pages:
            response = self.app.get(page)
            self.assertEqual(500, response.status_code)
            self.assertIn("Not logged in.", response.data)

if __name__ == '__main__':
    unittest.main()
