from bs4 import BeautifulSoup

from . import BaseTestClass

from model.Connection import Connection

db = Connection()

class TestErreserba(BaseTestClass):

	def test_erreserben_historiala_kontsultatu(self):
		# testak:
		# 			1. historiala hutsik dauka
		#			2. historiala dauka
		# [1]
		self.sartu('inigoduenas', 'inigoduenas')
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(0, len(page.find('div', class_='row').find_all('div', class_='card')))
		self.irten()
		# [2]
		self.sartu('ikertranchand', 'ikertranchand')
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(2, len(page.find('div', class_='row').find_all('div', class_='card')))
		self.irten()

	def test_liburua_erreserbatu(self):
		# testak:
		# 			1. liburua erreserbatu
		erabiltzaileID = 'inigoduenas'
		self.sartu(erabiltzaileID, 'inigoduenas')
		# [1]
		params = {
			'titulua': "Viaje con turbulencias"
		}
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(db.select("SELECT count() FROM Erreserba WHERE erabiltzaileizena = ?", (erabiltzaileID,))[0][0],
						 len(page.find('div', class_='row').find_all('div', class_='card-body'))//2)
		res = self.client.get('/catalogue')
		self.assertEqual(200, res.status_code)
		res = self.client.get('/liburua', query_string=params)
		self.assertEqual(302, res.status_code)
		res = self.client.get('/erreserbak')
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(db.select("SELECT count() FROM Erreserba WHERE erabiltzaileizena = ?", (erabiltzaileID,))[0][0],
						 len(page.find('div', class_='row').find_all('div', class_='card-body'))//2)
		# liburu bat kendu
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		lid = page.find('h5', class_='card-title')
		params = {
			'id': str(lid.text.split()[-1])
		}
		res = self.client.get('/erreserbak', query_string = params)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/erreserbak')
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(db.select("SELECT count() FROM Erreserba WHERE erabiltzaileizena = ?", (erabiltzaileID,))[0][0],
						 len(page.find('div', class_='row').find_all('div', class_='card-body'))//2)
		self.irten()

	def test_liburua_bueltatu(self):
		erabiltzaileID = 'inigoduenas'
		self.sartu(erabiltzaileID, 'inigoduenas')
		params = {
			'titulua': "Ligeros libertinajes sabaticos"
		}
		res = self.client.get('/liburua', query_string=params)
		self.assertEqual(302, res.status_code)

		# [1]: Jada erreserbatuta dago
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		lid = page.find('h5', class_='card-title')
		params = {
			'id': str(lid.text.split()[-1])
		}
		res = self.client.get('/erreserbak', query_string=params)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(db.select("SELECT count() FROM Erreserba WHERE erabiltzaileizena = ?", (erabiltzaileID,))[0][0],
						 len(page.find('div', class_='row').find_all('div', class_='card-body'))//2)

		self.irten()
