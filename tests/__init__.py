import unittest
from controller import webServer
from model import Connection

class BaseTestClass(unittest.TestCase):
	def setUp(self):
		self.app = webServer.app
		self.client = self.app.test_client()
		self.db = Connection()
		
	def tearDown(self):
		pass

	def login(self, erabiltzaileID, password):
		return self.client.post('/login', data=dict(
			erabiltzaileID=erabiltzaileID,
			password=password
		))

	def logout(self):
		return self.client.get('/logout')

	def sartu(self, erabiltzaileID, password):
		res = self.login(erabiltzaileID, password)

	def irten(self):
		res = self.logout()
		self.assertEqual(302, res.status_code)
		self.assertEqual('/', res.location)
		res = self.client.get('/')
		self.assertNotIn('token', ''.join(res.headers.values()))
		self.assertNotIn('time', ''.join(res.headers.values()))
