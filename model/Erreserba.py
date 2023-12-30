class Erreserba:
	def __init__(self, liburuID, erabiltzaileIzena, hasieraData, bukaeraData):
		self.liburuID = liburuID
		self.erabiltzaileIzena = erabiltzaileIzena
		self.hasieraData = hasieraData
		self.bukaeraData = bukaeraData

	def __str__(self):
		return f"{self.liburuID}:{self.erabiltzaileIzena}:{self.hasieraData}-{self.bukaeraData}"
