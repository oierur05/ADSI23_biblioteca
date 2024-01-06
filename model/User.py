import datetime
from .Connection import Connection
from .tools import hash_password

db = Connection()

class Session:
	def __init__(self, hash, time):
		self.hash = hash
		self.time = time

	def __str__(self):
		return f"{self.hash} ({self.time})"

class User:
	def __init__(self, username, argazkia, administratzaileaDa):
		self.username = username
		self.argazkia = argazkia
		self.administratzaileaDa = administratzaileaDa

	def __str__(self):
		return f"{self.username}"

	def validate_session(self, session_hash):
		s = db.select("SELECT * from Saioa WHERE erabiltzaileizena = ? AND hash = ?", (self.username, session_hash))
		if len(s) > 0:
			now = float(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f"))
			session_hash_new = hash_password(str(self.username) + str(now))
			db.update("UPDATE Saioa SET hash = ?, data=? WHERE hash = ? and erabiltzaileizena = ?", (session_hash_new, now, session_hash, self.username))
			return Session(session_hash_new, now)
		else:
			return None

	def delete_session(self, session_hash):
		db.delete("DELETE FROM Saioa WHERE hash = ? AND erabiltzaileizena = ?", (session_hash, self.username))

	def sortuSaioa(self):
		now = float(datetime.datetime.now().time().strftime("%Y%m%d%H%M%S.%f"))
		session_hash = hash_password(str(self.username)+str(now))
		db.insert("INSERT INTO Saioa VALUES (?, ?, ?)", (session_hash, self.username, now))
		return Session(session_hash, now)

	def eskaeraKudeatu(self, onartuDa, erabiltzaileID):
		if onartuDa:
			db.update("UPDATE Laguna SET onartua = 'bai' WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?) OR (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
					  (self.username,erabiltzaileID,erabiltzaileID,self.username))
		else:
			db.delete("DELETE FROM Laguna WHERE onartua = 'ez' AND (erabiltzaile1 = ? AND erabiltzaile2 = ?) OR (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
					  (self.username,erabiltzaileID,erabiltzaileID,self.username))
