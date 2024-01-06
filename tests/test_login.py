from . import BaseTestClass
from bs4 import BeautifulSoup

class TestLogin(BaseTestClass):

	def test_login_page_unauthentificated(self):
		res = self.client.get('/login')
		self.assertEqual(200, res.status_code)
		self.assertNotIn('token', ''.join(res.headers.values()))
		self.assertNotIn('time', ''.join(res.headers.values()))
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertIsNotNone(page.find('form').find('input', id='erabiltzaileID'))
		self.assertIsNotNone(page.find('form').find('input', id='password'))
		self.assertIsNotNone(page.find('form').find('button', type='submit'))

	def test_login_success(self):
		res = self.login('inigoduenas', 'inigoduenas')
		self.assertEqual(302, res.status_code)
		self.assertEqual('/perfila', res.location)
		self.assertIn('token', ''.join(res.headers.values()))
		self.assertIn('time', ''.join(res.headers.values()))
		token = [x.split("=")[1].split(";")[0] for x in res.headers.values() if 'token' in x][0]
		time = float([x.split("=")[1].split(";")[0] for x in res.headers.values() if 'time' in x][0])
		res = self.db.select(f"SELECT erabiltzaileizena FROM Saioa WHERE hash='{token}' AND data={time}")
		self.assertEqual(1, len(res))
		self.assertEqual('inigoduenas', res[0][0])
		res2 = self.client.get('/')
		page = BeautifulSoup(res2.data, features="html.parser")
		self.assertEqual('inigoduenas', page.find('header').find('ul').find_all('li')[-3].get_text())
		self.irten()

	def test_login_failure(self):
		res = self.login('inigoduenas', 'badpassword')
		self.assertEqual(302, res.status_code)
		self.assertEqual('/login', res.location)
		self.assertNotIn('token', ''.join(res.headers.values()))
		self.assertNotIn('time', ''.join(res.headers.values()))

	def test_log_out(self):
		res = self.login('inigoduenas', 'inigoduenas')
		self.assertEqual(302, res.status_code)
		self.assertEqual('/perfila', res.location)
		res2 = self.client.get('/')
		self.assertIn('token', ''.join(res2.headers.values()))
		self.assertIn('time', ''.join(res2.headers.values()))
		res3 = self.client.get('/logout')
		self.assertEqual(302, res3.status_code)
		self.assertEqual('/', res3.location)
		res4 = self.client.get('/')
		self.assertNotIn('token', ''.join(res4.headers.values()))
		self.assertNotIn('time', ''.join(res4.headers.values()))
