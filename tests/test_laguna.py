from . import BaseTestClass

from bs4 import BeautifulSoup

from model import Connection

db = Connection()

class TestLagunak(BaseTestClass):

	def test_lagun_eskaera(self):
		params1 = {
			'lagunIzena': "ikertranchand"
		}
		params2 = {
			'eskBidali': "ikertranchand"
		}
		params3 = {
			'lagunIzena': "inigoduenas"
		}
		params4 = {
			'eskBidali': "inigoduenas"
		}
		params5 = {
			'lagunIzena': "irune"
		}
		params6 = {
			'eskBidali': "irune"
		}

		# erabiltzailea existitzen da, ez da zure laguna eta ez zara zu
		eskaerak1 = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
					  ('irune','ikertranchand'))[0][0]
		self.sartu('irune', 'irune')
		res = self.client.get('/lagunak', query_string=params1)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(3, len(page.find_all('h5', class_='card-title')))
		res = self.client.get('/lagunak', query_string=params2)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(2, len(page.find_all('h5', class_='card-title')))
		eskaerak2 = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
					  ('irune','ikertranchand'))[0][0]
		self.assertEqual(eskaerak1,eskaerak2 - 1)
		self.irten()

		# erabiltzailea jada zure laguna da
		eskaerak1 = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
							  ('irune', 'inigoduenas'))[0][0]
		self.sartu('irune', 'irune')
		res = self.client.get('/lagunak', query_string=params3)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(3, len(page.find_all('h5', class_='card-title')))
		res = self.client.get('/lagunak', query_string=params4)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(2, len(page.find_all('h5', class_='card-title')))
		eskaerak2 = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
							  ('irune', 'ikertranchand'))[0][0]
		self.assertEqual(eskaerak1, eskaerak2)
		self.irten()

		# erabiltzailea zu zara
		eskaerak1 = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
							  ('irune', 'irune'))[0][0]
		self.sartu('irune', 'irune')
		res = self.client.get('/lagunak', query_string=params5)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(3, len(page.find_all('h5', class_='card-title')))
		res = self.client.get('/lagunak', query_string=params6)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(2, len(page.find_all('h5', class_='card-title')))
		eskaerak2 = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
							  ('irune', 'irune'))[0][0]
		self.assertEqual(eskaerak1, eskaerak2)
		self.irten()

		# erabiltzaileak jada zure eskaera bat dauka
		eskaerak1 = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
							  ('irune', 'ikertranchand'))[0][0]
		self.sartu('irune', 'irune')
		res = self.client.get('/lagunak', query_string=params1)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(3, len(page.find_all('h5', class_='card-title')))
		res = self.client.get('/lagunak', query_string=params2)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(2, len(page.find_all('h5', class_='card-title')))
		eskaerak2 = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
							  ('irune', 'ikertranchand'))[0][0]
		self.assertEqual(eskaerak1, eskaerak2)
		self.irten()

		db.delete(
			"DELETE FROM Laguna WHERE onartua = 'ez' AND (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
			('irune', 'ikertranchand'))

	def test_eskaerak_kontsultatu(self):
		params1 = {
			'lagunIzena': "ikertranchand"
		}
		params2 = {
			'eskBidali': "ikertranchand"
		}
		self.sartu('irune', 'irune')
		res = self.client.get('/lagunak', query_string=params1)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(3, len(page.find_all('h5', class_='card-title')))
		res = self.client.get('/lagunak', query_string=params2)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(2, len(page.find_all('h5', class_='card-title')))
		eskaerak = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile2 = ? AND onartua = ?)",
							 ('irune', 'ez'))[0][0]
		self.assertEqual(0, eskaerak)
		self.irten()

		self.sartu('ikertranchand', 'ikertranchand')
		res = self.client.get('/lagunak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(4, len(page.find_all('h5', class_='card-title')))
		eskaerak = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
							  ('irune', 'ikertranchand'))[0][0]
		self.assertEqual(1, eskaerak)
		self.irten()

		db.delete(
			"DELETE FROM Laguna WHERE onartua = 'ez' AND (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
			('irune', 'ikertranchand'))

	def test_eskaerak_kudeatu(self):
		params1 = {
			'lagunIzena': "ikertranchand"
		}
		params2 = {
			'eskBidali': "ikertranchand"
		}
		params3 = {
			'lagunIzena': "oierur_05"
		}
		params4 = {
			'eskBidali': "oierur_05"
		}
		self.sartu('irune', 'irune')
		res = self.client.get('/lagunak', query_string=params1)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/lagunak', query_string=params2)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/lagunak', query_string=params3)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/lagunak', query_string=params4)
		self.assertEqual(200, res.status_code)
		self.irten()

		params1 = {
			'onartu': "irune"
		}
		params2 = {
			'ezeztatu': "irune"
		}

		# eskaera bat onartu
		self.sartu('ikertranchand', 'ikertranchand')
		res = self.client.get('/lagunak', query_string=params1)
		self.assertEqual(200, res.status_code)
		lagunaDa = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ? AND onartua = ?)",
				  ('irune', 'ikertranchand', 'bai'))[0][0]
		self.assertEqual(1, lagunaDa)
		self.irten()

		db.delete(
			"DELETE FROM Laguna WHERE onartua = 'bai' AND (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
			('irune', 'ikertranchand'))
		db.delete(
			"DELETE FROM Laguna WHERE onartua = 'bai' AND (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
			('ikertranchand', 'irune'))

		# eskaera bat ezeztatu
		self.sartu('oierur_05', 'oierur_05')
		res = self.client.get('/lagunak', query_string=params2)
		self.assertEqual(200, res.status_code)
		lagunaDa = db.select("SELECT count() FROM LAGUNA WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
				  ('irune', 'oierur_05'))[0][0]
		self.assertEqual(0, lagunaDa)
		self.irten()

		



