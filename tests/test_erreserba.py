from . import BaseTestClass

from controller.LibraryController import LibraryController
library = LibraryController()

class TestErreserba(BaseTestClass):
	
	def test_erreserben_historiala_kontsultatu(self):
		# TODO: falta la parte de liburuak en html asiq...
		# testak:
		# 			historiala hutzik dauka
		#			historiala dauka
		self.assertTrue(False)

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
		# 			liburua ez da existizen
		#         zuzena:
		# 			liburua existizen da eta erreserbatuta dago
		self.assertTrue(False)
