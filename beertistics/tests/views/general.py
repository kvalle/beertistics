import unittest
from json import loads
from beertistics import app
from beertistics.tests.base import BeertisticsTestCase


class GeneralViewsTests(unittest.TestCase, BeertisticsTestCase):

    def setUp(self):
        self.commonSetUp()
        self.login()

    def test_frontpage(self):
        response = self.app.get('/')
        assert "<title>Overview" in response.data

    def test_about_page(self):
        response = self.app.get('/about')
        assert "<title>About" in response.data

    def test_that_all_api_pages_return_valid_json_and_200_response(self):
        pages = [str(rule) for rule in app.url_map.iter_rules()
                            if str(rule).startswith("/api")]
        for page in pages:
            response = self.app.get(page)
            self.assertEqual(200, response.status_code)
            try:
                loads(response.data)
            except:
                raise Exception("%s returned invalid Json" % page)

if __name__ == '__main__':
    unittest.main()
