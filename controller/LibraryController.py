import uuid

from model import Connection, Book, User
from model.Erreseina import Erreseina
from model.Erreserba import Erreserba
from model.Foroa import Foroa

db = Connection()


class LibraryController:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(LibraryController, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

# esto se utiliza en algun lau, y peta si se quita...
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

    def getErabiltzaile(self, erabiltzaileizena):
        user = db.select("SELECT * from Erabiltzailea WHERE erabiltzaileizena = ?", erabiltzaileizena)
        if len(user) == 0:
            return None

        user = user[0]

        return User(user[0], user[7], user[8])

    def get_user_cookies(self, token, time):
        user = db.select(
            "SELECT e.* from Erabiltzailea e, Saioa s WHERE e.z = s.user_id AND s.last_login = ? AND s.session_hash = ?",
            (time, token))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2])
        else:
            return None

    # FOROAK
    def getForoa(self, foroID):
        foroLista = db.select("SELECT * from Foroa WHERE id = ?", (foroID))

        if len(foroLista) == 0:
            return None

        foroa = foroLista[0]

        return Foroa(foroa[0], foroa[1], foroa[2], foroa[3], foroa[4])

    def getForoak(self, hitzGako):
        foroLista = db.select(
            "SELECT * from Foroa WHERE foroID LIKE ? OR erabiltzaileIzena LIKE ? OR izena LIKE ? OR deskribapena LIKE ? OR sorreraData LIKE ?",
            ('%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',
             '%' + hitzGako + '%',))

        return [Foroa(f[0], f[1], f[2], f[3], f[4]) for f in foroLista]

    def foroaSortu(self, fIzena, eIzena, deskribapena):
        db.insert("INSERT INTO Foroa VALUES(?,?,?,?)",
                  (self.idBerria(db.select("SELECT foroID FROM Foroa")), fIzena, eIzena, deskribapena))

    # LAGUNAK

    def setLagunEskaera(self, igorleID, jasotzaileID):
        eskaerak = db.select("SELECT erabiltzaile1 FROM Laguna "
                             "WHERE (erabiltzaile1 = ? AND erabiltzaile2 = ?) OR (erabiltzaile1 = ? AND erabiltzaile2 = ?)",
                             (igorleID, jasotzaileID, jasotzaileID, igorleID))
        if len(eskaerak) != 0:
            return
        db.insert("INSERT INTO Laguna(erabiltzaile1,erabiltzaile2) VALUES (?,?,false)", (igorleID, jasotzaileID))

    def getLagunEskaerak(self, erabiltzaileID):
        return [e[0] for e in db.select("SELECT erabiltzaile1 FROM Laguna WHERE onartua = false AND erabiltzaile2 = ?",
                                        (erabiltzaileID))]

    def getLagunak(self, erabiltzaileID):
        lista = [e[0] for e in db.select("SELECT erabiltzaile1 FROM Laguna WHERE onartua = true AND erabiltzaile2 = ?",
                                        (erabiltzaileID))]
        lista.extend([e[0] for e in db.select("SELECT erabiltzaile2 FROM Laguna WHERE onartua = true AND erabiltzaile1 = ?",
                           (erabiltzaileID))])
        return lista


    # ERRESERBAK

    def getErreserbak(self, erabiltzaileID):
        erreserbak = db.select("SELECT * from Erreserba WHERE erabiltzaileID = ?", erabiltzaileID)
        return [Erreserba(e[0], e[1], e[2], e[3]) for e in erreserbak]

    # ERRESEINAK

    def getErreseina(self, erabiltzaileID, liburuID):
        erreseinak = db.select("SELECT * from Erreseina WHERE erabiltzaileID = ? AND liburuID = ?",
                               (erabiltzaileID, liburuID))
        if len(erreseinak) == 0:
            return None
        e = erreseinak[0]
        return Erreseina(e[0], e[2], e[3], e[4])

    def getErreseinak(self, erabiltzaileID, liburuID):
        erreseinak = db.select("SELECT * FROM Erreseina WHERE erabiltzaileID = ? AND liburuID = ?",
                               (erabiltzaileID, liburuID))
        return [Erreseina(e[0], e[2], e[3], e[4]) for e in erreseinak]

    def erreseinaEguneratu(self, erabiltzaileID, liburuID, puntuazioa, testua):
        em = db.select("SELECT erreseinaID from Erreseina WHERE erabiltzaileID = ? AND liburuID = ?",
                       (erabiltzaileID, liburuID))

        if len(em) == 0:
            db.insert("INSERT INTO Erreseina (erreseinaID,puntuazioa,testua,likeKopurua) VALUES (?,?,?,?)",
                      (erabiltzaileID, liburuID, puntuazioa, testua, 0))
        else:
            db.update("UPDATE Erreseina SET puntuazioa = ?, testua = ? WHERE erabiltzaileID = ? AND liburuID = ?",
                      (puntuazioa, testua, erabiltzaileID, liburuID))

    # ADMINISTRATZAILE FUNTZIOAK

    def liburuBerriaGehitu(self, portada, izenburua, urtea, idazlea, sinopsia, PDF):
        lib = db.select("SELECT liburuID FROM Liburua WHERE izenburua = ? AND urtea = ? AND idazlea = ?",
                        (izenburua, urtea, idazlea, sinopsia))

        if len(lib) == 0:
            lID = self.idBerria(db.select("SELECT liburuID FROM Liburua"))
            db.insert("INSERT INTO Liburua VALUES(?,?,?,?,?,?,?)",
                      (lID, portada, izenburua, urtea, idazlea, sinopsia, PDF))
        else:
            raise Exception("ID hau duen liburu bat existitzen da jada.")

    def erabiltzaileBerriaSortu(self, eIzena, izenAbizenak, pasahitza, nan, tel, pElek, helb, argazkia,
                                administratzaileaDa):
        erabiltzaileak = db.select("SELECT * FROM Erabiltzaile WHERE erabiltzaileIzena = ?", eIzena)

        if len(erabiltzaileak) == 0:
            db.insert("INSERT INTO Erabiltzaile VALUES (?,?,?,?,?,?,?,?,?)",
                      (eIzena, izenAbizenak, pasahitza, nan, tel, pElek, helb, argazkia, administratzaileaDa))
        else:
            raise Exception("Erabiltzaile izena ez da baliozkoa.")

    def erabiltzaileaEzabatu(self, eIzena):
        erabiltzaileak = db.select("SELECT * FROM Erabiltzaile WHERE erabiltzaileIzena = ?", eIzena)

        if len(erabiltzaileak) == 0:
            raise Exception("Erabiltzailea ez da existitzen.")
        else:
            db.delete("DELETE FROM Erabiltzaile WHERE erabiltzaileIzena = ?", eIzena)

    # ERABILTZAILEAK

    def erabiltzaileBilatu(self, eIzena):
        erabiltzaileak = db.select("SELECT * from User WHERE izena = ?", eIzena)
        if len(erabiltzaileak) == 0:
            return None

        user = erabiltzaileak[0]

        return User(user[0], user[7], user[8])

    # LIBURUAK

    def getLiburuak(self, hitzGako):
        liburuak = db.select(
            "SELECT * from Book WHERE liburuID LIKE ? OR izenburua LIKE ? OR urtea LIKE ? OR idazlea LIKE ? OR sinopsia LIKE ?",
            ('%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',
             '%' + hitzGako + '%',))

        return [Book(b[0], b[1], b[2], b[3], b[4], b[5], b[6]) for b in liburuak]

    def getLiburua(self, liburuID):
        liburuak = db.select("SELECT * FROM Book WHERE liburuID = ?", liburuID)
        if len(liburuak) == 0:
            return None

        b = liburuak[0]

        return Book(b[0], b[1], b[2], b[3], b[4], b[5], b[6])

    # ID sortzailea
    def idBerria(self, idLista):
        idLista = map(int, idLista)

        idBerria = uuid.uuid4().int // 2 ** 16  # uuid.uuid4().hex[-4:]
        while idBerria in idLista:
            idBerria += 1  # = uuid.uuid4().int // 2**16
        return idBerria
