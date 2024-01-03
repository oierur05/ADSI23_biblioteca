from bs4 import BeautifulSoup

from . import BaseTestClass

from model import Connection

db = Connection()

class TestAdministratzailea(BaseTestClass):

    def test_aukerak_ikusi(self):
        # testak:
        #           1. erabiltzailea administratzailea da
        #           2. erabiltzailea ez da administratzailea
        # [1]
        self.sartu('juanbelio', 'juanbelio')
        res = self.client.get('/perfila')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(2, len(page.find_all('div', class_='card-body')))
        self.irten()
        # [2]
        self.sartu('irune', 'irune')
        res = self.client.get('/perfila')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(1, len(page.find_all('div', class_='card-body')))
        self.irten()

    def test_erabiltzaile_berria_sortu(self):
        # testak: erabiltzaile izen bakarra duen erabiltzaile berri bat sortzen da
        params = {
            'izenabizen': "iker",
            'argazkia': "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.redd.it%2Fc9qhc1n16l441.jpg&f=1&nofb=1&ipt=894c370726f56fba3c7ed7cc62af796192d35465677af8b3ebb73d3296ec4e82&ipo=images",
            'nan': "12345678-A",
            'telefonoa': 678678678,
            'helbidea': "Bilbao",
            'posta': "iker@iker.com",
            'erabIzena': "iker",
            'pasahitza': "su",
            'admin': False
        }
        self.assertEqual(0, db.select("SELECT Count() FROM ERABILTZAILEA WHERE erabiltzaileizena = ?", ("iker",))[0][0])
        self.sartu('juanbelio', 'juanbelio')
        res = self.client.get('/erabSortu', query_string=params)
        self.assertEqual(302, res.status_code)
        self.assertEqual(1, db.select("SELECT Count() FROM ERABILTZAILEA WHERE erabiltzaileizena = ?", ("iker",))[0][0])

        # erabiltzaile izen hori duen erabiltzaile bat existitzen da jada
        res = self.client.get('/erabSortu', query_string=params)
        self.assertEqual(302, res.status_code)
        self.assertEqual(1, db.select("SELECT Count() FROM ERABILTZAILEA WHERE erabiltzaileizena = ?", ("iker",))[0][0])

        db.select("DELETE FROM ERABILTZAILEA WHERE erabiltzaileizena = ?", ("iker",))
        self.irten()

    def test_erabiltzailea_ezabatu(self):
        # testak: okerra:
        #           ez da erabiltzailea ezabatu
        #         zuzena:
        #           erabiltzailea ezabatu da
        params = {
            'erabIzena': "iker"
        }

        db.insert("INSERT INTO ERABILTZAILEA(izenabizenak, erabiltzaileizena, pasahitza) VALUES(?,?,?)", ("Iker", "iker", "iker"))

        self.assertEqual(1, db.select("SELECT Count() FROM ERABILTZAILEA WHERE erabiltzaileizena = ?", ("iker",))[0][0])
        self.sartu('juanbelio', 'juanbelio')
        res = self.client.get('/erabEzabatu', query_string=params)
        self.assertEqual(302, res.status_code)
        self.assertEqual(0, db.select("SELECT Count() FROM ERABILTZAILEA WHERE erabiltzaileizena = ?", ("iker",))[0][0])
