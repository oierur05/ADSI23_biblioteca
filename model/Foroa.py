import datetime
from .Connection import Connection
from .Mezua import Mezua

db = Connection()

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
		s = db.select("SELECT * from Mezua WHERE foroID = ?", (self.foroID))
		return [Mezua(m[0], m[2], m[3]) for m in s]

	def gehituMezua(self, eIzena, testua):
		now = float(datetime.datetime.now().time().strftime("%Y%m%d%H%M%S.%f"))
		db.insert("INSERT INTO Mezua VALUES (?, ?, ?, ?)", (eIzena, self.foroID, now, testua))
		return Mezua(eIzena, now, testua)
