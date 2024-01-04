from bs4 import BeautifulSoup

from controller.LibraryController import LibraryController
from . import BaseTestClass

from model.Connection import Connection

db = Connection()
library = LibraryController()
class TestErreseina(BaseTestClass):

	def test_erreseinak_kontsultatu(self):
		# testak:
		# 			1. ez dira liburuaren erreseina guztiak agertzen
		# [1]
		liburua = {
			'titulua': "El Principe de la Niebla"
		}
		erabiltzaileID = 'juanbelio'
		self.sartu(erabiltzaileID, 'juanbelio')
		res = self.client.get('/catalogue', query_string=liburua)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		print(db.select("SELECT count() FROM Erreseina WHERE liburuid = ?", ("26903",))[0][0])
		print([i for i in page.find_all("h5", class_="card-title")])
		self.assertEqual(
			db.select("SELECT count() FROM Erreseina WHERE liburuid = ?", ("26903",))[0][0],
			len([i for i in page.find_all("h5", class_="card-title")]))
		self.irten()

	def test_erreseina_egin_editatu(self):
		# testak: okerra:
		# 			1. liburua erreseina egin
		# 			2. liburua erreseina aldatu
		# http://127.0.0.1:5000/liburua?testua=1&balorazioa=2&erreseinaegin=erreseinaegin&liburuid=1
		liburua = {
			'izenburua': "El Principe de la Niebla"
		}
		erreseina = {
			'testua': "oso ona",
			'balorazioa': "8",
			'erreseinaegin': "erreseinaegin",
			'liburuid': "26903"
		}
		erreseina_editatuta = {
			'testua': "Bikaina",
			'balorazioa': "10",
			'erreseinaegin': "erreseinaegin",
			'liburuid': "26903"
		}
		erabiltzaileID = 'juanbelio'
		self.sartu(erabiltzaileID, 'juanbelio')
		# [1]
		res = self.client.get('/liburua', query_string=erreseina)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/catalogue', query_string=liburua)
		page = BeautifulSoup(res.data, features="html.parser")
		print(page.find_all("h5", class_="card-title"))
		self.assertEqual(1, len([i for i in page.find_all("h5", class_="card-title") if i.text.__contains__("Puntuazioa: 8")]))
		# [2]
		res = self.client.get('/liburua', query_string=erreseina_editatuta)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/catalogue', query_string=liburua)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(1, len([i for i in page.find_all("h5", class_="card-title") if i.text.__contains__("Puntuazioa: 10")]))
		self.irten()
