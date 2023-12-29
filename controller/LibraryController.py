from model import Connection, Book, User
from model.Foroa import Foroa
from model.tools import hash_password

db = Connection()

class LibraryController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(LibraryController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance


	def search_books(self, title="", author="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
		res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count

	def getErabiltzaile(self, erabiltzaileID):
		user = db.select("SELECT * from User WHERE erabiltzaileID = ?", erabiltzaileID)
		return user.fetchone()

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2])
		else:
			return None

	# FOROAK
	def getForoa(self, foroID):
		foroLista = db.select("SELECT * from Foro WHERE id = ?", (foroID))

		if len(foroLista) == 0:
			return None

		foroa = foroLista[0]

		return Foroa(foroa[0], foroa[1], foroa[2], foroa[3], foroa[4])

	def getForoak(self, hitzGako):
		emaitzak = db.select("SELECT * from FOROA WHERE foroID LIKE ? OR erabiltzaileIzena LIKE ? OR izena LIKE ? OR deskribapena LIKE ? OR sorreraData LIKE ?", (
		'%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',))
		return emaitzak.fetchall()

	def foroaSortu(self, fID, fIzena, eIzena, deskribapena):
		foro = db.select("SELECT * FROM FOROA WHERE foroID = ?", fID)
		foroaDago = foro.fetchone()
		if foroaDago:
			raise Exception("ID hau duen foro bat existitzen da jada.")
		else:
			db.insert("INSERT INTO FOROA VALUES(?,?,?,?)", (fID,fIzena,eIzena,deskribapena))

	# LAGUNAK

	def setLagunEskaera(self, igorleID, jasotzaileID):
		db.insert("INSERT INTO LAGUNA(erabiltzaile1,erabiltzaile2) VALUES (?,?,?)", (igorleID, jasotzaileID))

	# ERRESERBAK

	def getErreserbak(self, erabiltzaileID):
		emaitzak = db.select("SELECT * from Erreserba WHERE erabiltzaileID = ?",erabiltzaileID)
		return emaitzak.fetchall()

	# ERRESEINAK

	def getErreseina(self, erreseinaID):
		emaitza = db.select("SELECT * from ERRESEINA WHERE erreseinaID = ?", erreseinaID)
		return emaitza.fetchone()

	def getErreseinak(self, erabiltzaileID):
		emaitza = db.select("SELECT * FROM ERRESEINA WHERE erabiltzaileID = ?",erabiltzaileID)
		return emaitza.fetchall()

	def erreseinaEguneratu(self, erreseinaID, puntuazioa, testua):
		em = db.select("SELECT * from ERRESEINA WHERE erreseinaID = ?", erreseinaID)
		erreseinaDago = em.fetchone()
		if erreseinaDago:
			db.update("UPDATE ERRESEINA SET puntuazioa = ?, testua = ? WHERE erreseinaID = ?",(puntuazioa,testua,erreseinaID))
		else:
			db.insert("INSERT INTO ERRESEINA (erreseinaID,puntuazioa,testua) VALUES (?,?,?)", (erreseinaID,puntuazioa,testua))

	# ADMINISTRATZAILE FUNTZIOAK

	def liburuBerriaGehitu(self, lID, portada, izenburua, urtea, idazlea, sinopsia, PDF):
		lib = db.select("SELECT * FROM LIBURUA WHERE liburuID = ?", lID)
		liburuaDago = lib.fetchone()
		if liburuaDago:
			raise Exception("ID hau duen liburu bat existitzen da jada.")
		else:
			db.insert("INSERT INTO LIBURUA VALUES(?,?,?,?,?,?,?)", (lID,portada,izenburua,urtea,idazlea,sinopsia,PDF))

	def erabiltzaileBerriaSortu(self, eIzena, izenAbizenak, pasahitza, nan, tel, pElek, helb, argazkia, administratzaileaDa):
		user = db.select("SELECT * FROM ERABILTZAILE WHERE erabiltzaileIzena = ?", eIzena)
		erabiltzaileaDago = user.fetchone()
		if erabiltzaileaDago:
			raise Exception("Erabiltzaile izena ez da baliozkoa.")
		else:
			db.insert("INSERT INTO ERABILTZAILE VALUES (?,?,?,?,?,?,?,?,?)", (eIzena,izenAbizenak,pasahitza,nan,tel,pElek,helb,argazkia,administratzaileaDa))

	def erabiltzaileaEzabatu(self, eIzena):
		user = db.select("SELECT * FROM ERABILTZAILE WHERE erabiltzaileIzena = ?", eIzena)
		erabiltzaileaDago = user.fetchone()
		if erabiltzaileaDago:
			db.delete("DELETE FROM ERABILTZAILEA WHERE erabiltzaileIzena = ?", eIzena)
		else:
			raise Exception("Erabiltzailea ez da existitzen.")

	# ERABILTZAILEAK

	def erabiltzaileBilatu(self, eIzena):
		emaitzak = db.select("SELECT * from User WHERE izena LIKE ?", (
		eIzena + '%',))
		return emaitzak.fetchall()

	# LIBURUAK

	def getLiburuak(self, hitzGako):
		emaitzak = db.select("SELECT * from BOOK WHERE liburuID LIKE ? OR izenburua LIKE ? OR urtea LIKE ? OR idazlea LIKE ? OR sinopsia LIKE ?", (
		'%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',))
		return emaitzak.fetchall()

	def getLiburua(self, liburuID):
		emaitza = db.select("SELECT * FROM BOOK WHERE liburuID = ?",liburuID)
		return emaitza.fetchone()