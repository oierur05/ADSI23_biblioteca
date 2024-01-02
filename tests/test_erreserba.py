from bs4 import BeautifulSoup

from . import BaseTestClass

from controller.LibraryController import LibraryController
library = LibraryController()

class TestErreserba(BaseTestClass):

	def test_erreserben_historiala_kontsultatu(self):
		# TODO: falta la parte de liburuak en html asiq...
		# testak:
		# 			1. historiala hutsik dauka
		#			2. historiala dauka
		# [1]
		self.sartu('numen_0', 'calvo')
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		print(page.find('div', class_='row').prettify())
		self.assertEqual(0, len(page.find('div', class_='row').find_all('div', class_='card')))
		self.irten()
		# [2]
		self.sartu('juanbelio', 'juan')
		res = self.client.get('/erreserbak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(0, len(page.find('div', class_='row').find_all('div', class_='card')))
		self.logout()

	def test_liburua_erreserbatu(self):
		# TODO: falta la parte de liburuak en html asiq...
		# testak: okerra:
		# 			liburua erreserbatuta dago
		#         zuzena:
		# 			liburua ez dago erreserbatuta
		self.assertTrue(False)

	def test_liburua_bueltatu(self):
		# TODO: falta la parte de liburuak en html asiq...
		# testak: okerra:
		# 			liburua ez dago erreserbatuta
		# 			liburua ez da existitzen
		#         zuzena:
		# 			liburua existitzen da eta erreserbatuta dago
		self.assertTrue(False)
