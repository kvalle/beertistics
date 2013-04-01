from beertistics import app
import hashlib

class BeertisticsTestCase():

    def commonSetUp(self):
        self.username = 'testuser'
        self.password = 'password'
        app.config['TESTING'] = True
        app.config['USERNAME'] = self.username
        app.config['PASSWORD'] = hashlib.sha1(self.password).hexdigest()
        self.app = app.test_client()

    def login(self, user=None, password=None):
        username = user or self.username
        password = password or self.password
        auth_data = dict(username=username, password=password)
        return self.app.post('/log-in', data=auth_data)
