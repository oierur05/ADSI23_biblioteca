class Mezua:
	def __init__(self, erabiltzaileIzena, data, testua):
		self.erabiltzaileIzena = erabiltzaileIzena
		self.foroID = data
		self.testua = testua

	def __str__(self):
		return f"{self.erabiltzaileIzena}:{self.testua}"
