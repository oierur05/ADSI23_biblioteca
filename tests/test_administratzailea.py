from bs4 import BeautifulSoup

from . import BaseTestClass

class TestAdministratzailea(BaseTestClass):

    def test_aukerak_ikusi(self):
        # testak:
        #           1. erabiltzailea administratzailea da
        #           2. erabiltzailea ez da administratzailea
        # [1]
        self.sartu('juanbelio', 'juan')
        res = self.client.get('/perfila')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(2, len(page.find_all('div', class_='card-body')))
        self.irten()
        # [2]
        self.sartu('numen_0', 'calvo')
        res = self.client.get('/perfila')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(1, len(page.find_all('div', class_='card-body')))
        self.irten()

    def test_erabiltzaile_berria_sortu(self):
        # testak: okerra:
        #           ez da erabiltzaile berri bat gehitzen
        #           erabiltzaile izen errepikatua duen erabiltzaile bat sortzen da
        #         zuzena:
        #           erabiltzaile izen bakarra duen erabiltzaile berri bat sortzen da
        self.sartu('juanbelio', 'juan')
        res = self.client.get('/erabSortu')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")



    def test_erabiltzailea_ezabatu(self):
        # testak: okerra:
        #           ez da erabiltzailea ezabatu
        #         zuzena:
        #           erabiltzailea ezabatu da
        self.assertTrue(False)
