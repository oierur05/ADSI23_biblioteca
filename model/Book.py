import datetime
from .Connection import Connection
from .Author import Author

db = Connection()

class Book:
	def __init__(self, id, portada, izenburua, urtea, idazlea, sinopsia, PDF):
		self.id = id
		self.portada = portada
		self.izenburua = izenburua
		self.urtea = urtea
		self.idazlea = idazlea
		self.sinopsia = sinopsia
		self.PDF = PDF

	@property
	def author(self):
		if type(self._author) == int:
			em = db.select("SELECT * from Author WHERE id=?", (self._author,))[0]
			self._author = Author(em[0], em[1])
		return self._author

	@author.setter
	def author(self, value):
		self._author = value

	def __str__(self):
		return f"{self.id}"

	def erreserbatu(self, erabiltzaileID):
		liburuIDLista = db.select("SELECT * from Kopiafisikoa WHERE liburuid = ?", (self.id,))
		if len(liburuIDLista) == 0:
			return

		liburuid = -1
		for k in liburuIDLista:
			res = db.select("SELECT * FROM Erreserba WHERE kopiafisikoid = ?", (k[0],))
			if len(res) == 0:
				liburuid = k[0]

		if liburuid == -1:
			return

		now = datetime.datetime.now().date()
		end = now + datetime.timedelta(days=14)

		db.insert("INSERT INTO Erreserba VALUES (?, ?, ?, ?)", (liburuid, erabiltzaileID, now, end,))

	def bueltatu(self, erabiltzaileID, kopiaid):
		#liburuIDLista = db.select("SELECT * from Kopiafisikoa WHERE liburuid = ?", (self.id,))
		#if len(liburuIDLista) == 0:
		#	return

		#liburuID = liburuIDLista[0][0]

		db.delete("DELETE FROM Erreserba WHERE kopiafisikoid = ? AND erabiltzaileizena = ?",
				  (kopiaid,erabiltzaileID,))
