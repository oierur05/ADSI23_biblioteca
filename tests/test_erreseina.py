from bs4 import BeautifulSoup

from . import BaseTestClass

from model.Connection import Connection

db = Connection()

class TestErreseina(BaseTestClass):
	
	def test_erreseinak_kontsultatu(self):
		# TODO
		# testak: okerra:
		# 			ez dira liburuaren erreseina guztiak agertzen
		#		  zuzena:
		#			liburuaren erreseina guztiak agertzen dira
		self.assertTrue(False)

	def test_erreseina_egin_editatu(self):
		# TODO
		# testak: okerra:
		# 			1. liburua erreseina egin
		# 			2. liburua erreseina aldatu
		# http://127.0.0.1:5000/liburua?testua=1&balorazioa=2&erreseinaegin=erreseinaegin&liburuid=1

		# [1]
		erabiltzaileID = 'juanbelio'
		self.sartu(erabiltzaileID, 'juan')
		res = self.client.get('/erreserbak')
		page = BeautifulSoup(res.data, features="html.parser")
		lid = page.find('h5', class_='card-title')
		print(lid)
		params = {
			'testua': "oso ona",
			'balorazioa': "8",
			'erreseinaegin': 'erreseinaegin',
			'liburuid': str(db.select("SELECT liburuid FROM Kopiafisikoa WHERE kopiaid = ?", (str(lid.text.split()[-1]),))[0][0])
		}
		res = self.client.get('/erreserbak', query_string=params)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		print(params)
		self.irten()
