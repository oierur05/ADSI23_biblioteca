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
		# print(db.select("SELECT count() FROM Erreseina WHERE liburuid = ?", ("26903",))[0][0])
		# print([i for i in page.find_all("h5", class_="card-title")])
		self.assertEqual(
			db.select("SELECT count() FROM Erreseina WHERE liburuid = ?", ("26903",))[0][0],
			len([i for i in page.find_all("h5", class_="card-title")])-1)
		self.irten()

	def test_erreseina_egin_editatu(self):
		# testak:
		# 			1. liburua erreseina egin
		# 			2. liburua erreseina aldatu
		liburua1 = {
			'titulua': "El Principe de la Niebla"
		}
		liburua2 = {
			'titulua': "Así es la p*ta vida: El libro de ANTI-autoayuda"
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
		komentariorik_ez = {
			'testua': "",
			'balorazioa': "7",
			'erreseinaegin': "erreseinaegin",
			'liburuid': "42614"
		}
		puntuaziorik_ez = {
			'testua': "Izugarria",
			'balorazioa': "",
			'erreseinaegin': "erreseinaegin",
			'liburuid': "42614"
		}
		erabiltzaileID = 'juanbelio'
		self.sartu(erabiltzaileID, 'juanbelio')
		# [1]
		res = self.client.get('/liburua', query_string=erreseina)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/catalogue', query_string=liburua1)
		page = BeautifulSoup(res.data, features="html.parser")
		# print(page.find_all("h5", class_="card-title"))
		self.assertEqual(1, len([i for i in page.find_all("h5", class_="card-title") if i.text.__contains__("Puntuazioa: 8")]))
		# [2]
		res = self.client.get('/liburua', query_string=erreseina_editatuta)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/catalogue', query_string=liburua1)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(2, len([i for i in page.find_all("h5", class_="card-title") if i.text.__contains__("Puntuazioa: 10")]))

		db.select("DELETE FROM ERRESEINA WHERE erabiltzaileizena = ? AND liburuid = ? AND testua = ?",
				("juanbelio", 26903, "Bikaina"))

		# [3]
		res = self.client.get('/liburua', query_string=komentariorik_ez)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/catalogue', query_string=liburua2)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(1, len([i for i in page.find_all("h5", class_="card-title") if
								i.text.__contains__("Puntuazioa: 7")]))

		db.select("DELETE FROM ERRESEINA WHERE erabiltzaileizena = ? AND liburuid = ? AND puntuazioa = ?",
				("juanbelio", 42614, "7"))

		# [4]
		res = self.client.get('/liburua', query_string=puntuaziorik_ez)
		self.assertEqual(302, res.status_code)
		res = self.client.get('/catalogue', query_string=liburua2)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(0, len([i for i in page.find_all("h6", class_="card-subtitle") if
								i.text.__contains__("Erreseina: Izugarria")]))
		self.irten()
