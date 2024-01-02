from bs4 import BeautifulSoup

from . import BaseTestClass

from controller.LibraryController import LibraryController
library = LibraryController()

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
		# testak: okerra:
		# 			1. liburua erreserbatuta dago
		#         zuzena:
		# 			2. liburua ez dago erreserbatuta
		self.sartu('numen_0', 'calvo')
		# [2]
		params = {
			'titulua': "Ligeros libertinajes sabaticos"
		}
		res = self.client.get('/catalogue', query_string = params)
		self.assertEqual(200, res.status_code)
		res = self.client.get('/liburua', query_string = params)
		print(res.headers)
		page = BeautifulSoup(res.data, features="html.parser")
		#self.assertEqual(0, len(page.find('div', class_='row').find_all('div', class_='card')))
		# [1]
		self.irten()
		self.assertTrue(False)

	def test_liburua_bueltatu(self):
		# testak: okerra:
		# 			liburua ez dago erreserbatuta
		# 			liburua ez da existitzen
		#         zuzena:
		# 			liburua existitzen da eta erreserbatuta dago
		self.assertTrue(False)
