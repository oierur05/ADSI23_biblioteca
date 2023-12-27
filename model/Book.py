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
		return f"{self.title} ({self.author})"

	def erreserbatu(erabiltzaileID):
		# HAY QUE HACERLO
		return