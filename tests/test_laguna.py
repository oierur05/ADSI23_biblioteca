from . import BaseTestClass
from bs4 import BeautifulSoup
class TestLagunak(BaseTestClass):

	def test_lagun_eskaera(self):
		res = self.client.get('/perfila')
		self.assertEqual(200, res.status_code)	 # esto peta siempre, mucho animo grupo ( ·_·)b
		page = BeautifulSoup(res.data, features="html.parser")
		# TODO: falta la parte de lagunas en html asiq...
		# testak: okerra:
		# 			erabiltzailea ez da existitze
		# 			erabiltzailea jada zure laguna da
		# 			erabiltzailea zu zara
		#			erabiltzaileak jada zure eskaera bat dauka
		# 			erabiltzaileak zuri eskaera bat bidali dizu
		#         zuzena:
		# 			erabiltzailea existitzen da, ez da zure laguna eta ez da zure berdina
		self.assertTrue(False)

	def test_eskaerak_kontsultatu(self):
		res = self.client.get('/perfila')
		self.assertEqual(200, res.status_code)	 # esto peta siempre, mucho animo grupo ( ·_·)b
		page = BeautifulSoup(res.data, features="html.parser")
		# TODO: falta la parte de lagunas en html asiq...
		# testak:
		# 			ez dago eskaerarik
		# 			hainbat eskaera daude
		self.assertTrue(False)

	def test_eskaerak_kudeatu(self):
		res = self.client.get('/perfila')
		self.assertEqual(200, res.status_code)	 # esto peta siempre, mucho animo grupo ( ·_·)b
		page = BeautifulSoup(res.data, features="html.parser")
		# TODO: falta la parte de lagunas en html asiq...
		# testak:
		# 			eskaera ezeztatu
		# 			eskaera onartu
		self.assertTrue(False)


		



