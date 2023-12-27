class Foroa:
	def __init__(self, foroID, erabiltzaileIzena, izena, deskribapena, sorreraData):
		self.foroID = foroID
		self.erabiltzaileIzena = erabiltzaileIzena
		self.izena = izena
		self.deskribapena = deskribapena
		self.sorreraData = sorreraData

	def __str__(self):
		return f"{self.foroID}:{self.izena}"

	def getMezuak(self):
		# TODO
		pass

	def gehituMezua(self, eIzena, testua):
		# TODO
		pass