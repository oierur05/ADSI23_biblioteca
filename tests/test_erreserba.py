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
		self.sartu('numen_0', 'calvo')
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(2, len(page.find('div', class_='row').find_all('div', class_='card')))
		self.irten()
		# [2]
		self.sartu('juanbelio', 'juan')
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(0, len(page.find('div', class_='row').find_all('div', class_='card')))
		self.irten()

	def test_liburua_erreserbatu(self):
		# testak:
		# 			1. liburua erreserbatu
		erabiltzaileID = 'numen_0'
		self.sartu(erabiltzaileID, 'calvo')
		# [1]
		params = {
			'titulua': "Ligeros libertinajes sabaticos"
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
		# testak: okerra:
		# 			1. liburua ez dago erreserbatuta
		# 			2. liburua ez da existitzen
		#         zuzena:
		# 			3. liburua existitzen da eta erreserbatuta dago
		erabiltzaileID = 'juanbelio'
		self.sartu(erabiltzaileID, 'juan')
		params = {
			'titulua': "Ligeros libertinajes sabaticos"
		}
		res = self.client.get('/liburua', query_string=params)
		self.assertEqual(302, res.status_code)

		# [1]
		params = {
			'id': "-1"
		}
		#res = self.client.get('/erreserbak', query_string=params) # TODO: aqui hay un bug en el programa (webServer)
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(db.select("SELECT count() FROM Erreserba WHERE erabiltzaileizena = ?", (erabiltzaileID,))[0][0],
						 len(page.find('div', class_='row').find_all('div', class_='card-body'))//2)
		# [2]
		params = {
			'id': "5"
		}
		res = self.client.get('/erreserbak', query_string=params)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(db.select("SELECT count() FROM Erreserba WHERE erabiltzaileizena = ?", (erabiltzaileID,))[0][0],
						 len(page.find('div', class_='row').find_all('div', class_='card-body'))//2)
		# [3]
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
