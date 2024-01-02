import uuid

from model import Connection, Book, User
from model.Erreseina import Erreseina
from model.Erreserba import Erreserba
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

#	def search_books(self, title="", author="", limit=6, page=0):
#		count = db.select("""
#				SELECT count()
#				FROM Book b, Author a
#				WHERE b.author=a.id
#					AND b.title LIKE ?
#					AND a.name LIKE ?
#		""", (f"%{title}%", f"%{author}%"))[0][0]
#		res = db.select("""
#				SELECT b.*
#				FROM Book b, Author a
#				WHERE b.author=a.id
#					AND b.title LIKE ?
#					AND a.name LIKE ?
#				LIMIT ? OFFSET ?
#		""", (f"%{title}%", f"%{author}%", limit, limit*page))
#		books = [
#			Book(b[0],b[1],b[2],b[3],b[4])
#			for b in res
#		]
#		return books, count

    def getErabiltzaile(self, erabiltzaileizena, pasahitza):
        user = db.select("SELECT * from Erabiltzailea WHERE erabiltzaileizena = ? AND pasahitza = ?",
                         (erabiltzaileizena, pasahitza))
        if len(user) == 0:
            return None

        #user = user[0]

        return User(user[0][0], user[0][7], user[0][8])

    def get_user_cookies(self, token, time):
        user = db.select(
            "SELECT e.* from Erabiltzailea e, Saioa s WHERE e.erabiltzaileizena = s.erabiltzaileizena AND s.data = ? AND s.hash = ?",
            (time, token))
        if len(user) > 0:
            return User(user[0][0], user[0][7], user[0][8])
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
            "SELECT * from Foroa WHERE id LIKE ? OR erabiltzaileIzena LIKE ? OR izena LIKE ? OR deskribapena LIKE ? OR sorreraData LIKE ?",
            ('%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',
             '%' + hitzGako + '%',))

        count = db.select(
            "SELECT count() from Foroa WHERE id LIKE ? OR erabiltzaileIzena LIKE ? OR izena LIKE ? OR deskribapena LIKE ? OR sorreraData LIKE ?",
            ('%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',
             '%' + hitzGako + '%',))[0][0]

        return [Foroa(f[0], f[1], f[2], f[3], f[4]) for f in foroLista], count

    def foroaSortu(self, fIzena, eIzena, deskribapena):
        db.insert("INSERT INTO Foroa VALUES(?,?,?,?)",
                  (self.idBerria(db.select("SELECT foroID FROM FOROA")), fIzena, eIzena, deskribapena))

    # LAGUNAK

    def setLagunEskaera(self, igorleID, jasotzaileID):
        db.insert("INSERT INTO Laguna(erabiltzaile1,erabiltzaile2) VALUES (?,?,?)", (igorleID, jasotzaileID))

    # ERRESERBAK

    def getErreserbak(self, erabiltzaileID):
        erreserbak = db.select("SELECT * from Erreserba WHERE erabiltzaileizena = ?", (erabiltzaileID,))
        return [Erreserba(e[0], e[1], e[2], e[3]) for e in erreserbak]

    # ERRESEINAK

    def getErreseina(self, erabiltzaileID, liburuID):
        erreseinak = db.select("SELECT * from Erreseina WHERE erabiltzaileID = ? AND liburuID = ?",
                               (erabiltzaileID, liburuID))
        if len(erreseinak) == 0:
            return None
        e = erreseinak[0]
        return Erreseina(e[0], e[2], e[3], e[4])

    def getErreseinak(self, liburuID):
        erreseinak = db.select("SELECT * FROM Erreseina WHERE liburuID = ?",
                               (liburuID,))
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

    def erreseinaLikeGehitu(self, erabiltzaileID, liburuID):
        em = db.select("UPDATE Erreseina SET likeKopurua = likeKopurua + 1 WHERE erabiltzaileID = ? AND liburuID = ?",
                       (erabiltzaileID, liburuID))

    # ADMINISTRATZAILE FUNTZIOAK

    def liburuBerriaGehitu(self, portada, izenburua, urtea, idazlea, sinopsia, PDF):
        lib = db.select("SELECT count(liburuid) FROM Liburua WHERE izenburua = ? AND urtea = ? AND idazlea = ?",
                        (izenburua, urtea, idazlea,))[0][0]
        if lib == 0:
            lID = self.idBerria([i[0] for i in db.select("SELECT liburuID FROM LIBURUA")])
            db.insert("INSERT INTO Liburua VALUES(?,?,?,?,?,?,?)",
                      (lID, portada, izenburua, urtea, idazlea, sinopsia, PDF,))
            kID = self.idBerria([i[0] for i in db.select("SELECT kopiaid FROM Kopiafisikoa")])
            db.insert("INSERT INTO Kopiafisikoa VALUES(?,?)",
                      (kID, lID,))
        else:
            raise Exception("ID hau duen liburu bat existitzen da jada.")

    def erabiltzaileBerriaSortu(self, eIzena, izenAbizenak, pasahitza, nan,
                                                         tel, pElek, helb, argazkia, administratzaileaDa):
        erabiltzaileak = db.select("SELECT count(erabiltzaileizena) FROM Erabiltzailea WHERE erabiltzaileizena = ?", (eIzena,))[0][0]
        if erabiltzaileak == 0:
            db.insert("INSERT INTO Erabiltzailea VALUES (?,?,?,?,?,?,?,?,?)",
                      (eIzena, izenAbizenak, pasahitza, nan, tel, pElek, helb, argazkia, administratzaileaDa,))
        else:
            raise Exception("Erabiltzailea jadanik existitzen zen.")

    def erabiltzaileaEzabatu(self, eIzena):
        erabiltzaileak = db.select("SELECT count(erabiltzaileizena) FROM Erabiltzailea WHERE erabiltzaileizena = ?", (eIzena,))[0][0]
        if erabiltzaileak == 0:
            raise Exception("Erabiltzailea ez da existitzen.")
        else:
            db.delete("DELETE FROM Erabiltzailea WHERE erabiltzaileizena = ?", (eIzena,))

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
            "SELECT * from Liburua WHERE liburuID LIKE ? OR izenburua LIKE ? OR urtea LIKE ? OR idazlea LIKE ? OR sinopsia LIKE ?",
            ('%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',
             '%' + hitzGako + '%',))

        count = db.select(
            "SELECT count() from Liburua WHERE liburuID LIKE ? OR izenburua LIKE ? OR urtea LIKE ? OR idazlea LIKE ? OR sinopsia LIKE ?",
            ('%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',
             '%' + hitzGako + '%',))[0][0]

        libs = [Book(b[0], b[1], b[2], b[3], b[4], b[5], b[6]) for b in liburuak]

        return libs, count

    def getLiburua(self, liburuID):
        liburuak = db.select("SELECT * FROM Liburua WHERE liburuid = ?", (liburuID,))
        if len(liburuak) == 0:
            return None

        b = liburuak[0]

        return Book(b[0], b[1], b[2], b[3], b[4], b[5], b[6])

    def getLiburuKopia(self, liburuID):
        liburua = db.select("SELECT liburuid FROM Kopiafisikoa WHERE kopiaid = ?", (liburuID,))
        if len(liburua) == 0:
            return None

        return self.getLiburua(liburua[0][0])

    def getLiburuKopiaID(self, liburuID):
        libID = self.getLiburuKopia(liburuID)
        if libID is None:
            return None
        return libID.id

    # ID sortzailea
    def idBerria(self, idLista):
        # idLista = map(int, idLista)

        idBerria = uuid.uuid4().int % (2 ** 16)  # uuid.uuid4().hex[-4:]
        while idBerria in idLista:
            idBerria += 1  # = uuid.uuid4().int // 2**16
        print(idBerria)
        return idBerria
