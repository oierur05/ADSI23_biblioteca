from bs4 import BeautifulSoup

from . import BaseTestClass

from model import Connection

db = Connection()

class TestForoa(BaseTestClass):

    def test_gaiak_kontsultatu(self):
        # sisteman dauden gai guztiak agertzen dira
        self.sartu('irune', 'irune')
        res = self.client.get('/foroak')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(3, len(page.find_all('div', class_='card-body')))
        self.irten()

        # gai zehatz bati buruzko foroak agertzen dira
        params = {
            'izenburua': "abentura"
        }
        self.sartu('irune', 'irune')
        res = self.client.get('/foroak', query_string=params)
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(1, len(page.find_all('div', class_='card-body')))
        self.irten()

    def test_gaiaren_mezuak_ikusi(self):
        # foro baten mezuak ikusi
        self.sartu('irune', 'irune')
        res = self.client.get('/foroak?foroID=1')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(3, len(page.find_all('h5', class_='card-title')))
        self.irten()

    def test_mezua_idatzi(self):
        komentario1 = {
            'mezua': "Agur!",
            'foroID': 48570
        }
        komentario2 = {
            'mezua': "",
            'foroID': 48570
        }
        res = self.client.get('/foroak?foroID=48570')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        mezu_kop = db.select("SELECT count() FROM MEZUA WHERE foroid = ? ", (48570,))[0][0]
        self.assertEqual(mezu_kop, len(page.find_all('h5', class_='card-title')))

        # erregistratu gabe mezua idatzi
        res = self.client.get('/foroak?foroID=48570')
        self.assertEqual(200, res.status_code)
        res = self.client.get('/foroa', query_string=komentario1)
        self.assertEqual(302, res.status_code)
        self.assertEqual('/login', res.location)
        res = self.client.get('/foroak?foroID=48570')
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(mezu_kop, len(page.find_all('h5', class_='card-title')))

        # mezu bat forora gehitzea
        self.sartu('irune', 'irune')
        res = self.client.get('/foroa', query_string=komentario1)
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(mezu_kop+1, len(page.find_all('h5', class_='card-title')))

        db.delete("DELETE FROM MEZUA WHERE erabiltzaileizena = ? AND foroid = ? AND testua = ?", ("irune", 48570, "Agur!"))

        # mezu bat forora gehitzea, komentario hutza (mezua == "")
        res = self.client.get('/foroa', query_string=komentario2)
        self.assertEqual(302, res.status_code)
        res = self.client.get('/foroak?foroID=48570')
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(mezu_kop, len(page.find_all('h5', class_='card-title')))

        self.irten()

