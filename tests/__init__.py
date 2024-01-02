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
		return self.client.post('/logout', follow_redirects=True)

	def sartu(self, erabiltzaileID, password):
		res = self.login(erabiltzaileID, password)

	def irten(self):
		res = self.logout()
