from . import BaseTestClass

class TestAdministratzailea(BaseTestClass):

    def test_aukerak_ikusi(self):
        # testak: okerra:
        #           ezin ditu aukerak ikusi
        #         zuzena:
        #           aukerak ikus ditzake

    def test_erabiltzaile_berria_sortu(self):
        # testak: okerra:
        #           ez da erabiltzaile berri bat gehitzen
        #           erabiltzaile izen errepikatua duen erabiltzaile bat sortzen da
        #         zuzena:
        #           erabiltzaile izen bakarra duen erabiltzaile berri bat sortzen da

    def test_erabiltzailea_ezabatu(self):
        # testak: okerra:
        #           ez da erabiltzailea ezabatu
        #         zuzena:
        #           erabiltzailea ezabatu da
