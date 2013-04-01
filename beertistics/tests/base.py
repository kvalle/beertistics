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

    def login(self):
        data = dict(username=self.username, password=self.password)
        return self.app.post('/log-in', data=data)
