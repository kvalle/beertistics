from beertistics import app
import hashlib
import logging

class BeertisticsTestCase():

    def commonSetUp(self):
        app.logger.setLevel(logging.FATAL)
        app.config['TESTING'] = True
        app.config['UNTAPPD_STUB'] = True
        self.app = app.test_client()

    def get_with_redirect(self, url, limit=10):
        """
        Custom get method, since app.get seems to have a rather 
        low limit on how many redirects it will follow before a 
        "loop detected" is raised.
        """
        response = self.app.get('/stats/punchcard')
        while limit > 0 and 302 == response.status_code:
            next = response.location.strip("http://").strip(app.config["SERVER_NAME"])
            response = self.app.get(next)
            limit -= 1
        return response

    def login(self):
        self.app.get('/log-in', follow_redirects=True)
    