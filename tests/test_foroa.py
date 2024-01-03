from . import BaseTestClass

class TestForoa(BaseTestClass):

    def test_gaiak_kontsultatu(self):
        # sisteman dauden gai guztiak agertzen dira
        self.sartu('3ne', '3ne')
        res = self.client.get('/foroak')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(3, len(page.find_all('div', class_='card-body')))
        self.irten()

        # gai zehatz bati buruzko foroak agertzen dira
        params = {
            'abentura'
        }
        self.sartu('3ne', '3ne')
        res = self.client.get('/foroak', query_string=params)
        self.assertEqual(302, res.status_code)
        self.assertEqual(1, len(page.find_all('div', class_='card-body')))
        self.irten()

    def test_gaiaren_mezuak_ikusi(self):
    # testak: okerra:
    #           ez dira gaiaren mezu guztiak bistaratzen
    #         zuzena:
    #           gaiaren mezu guztiak bistaratzen dira
		self.assertTrue(False)

    def test_mezua_idatzi(self):
    # testak: okerra:
    #           mezua ez da gaira gehitu
    #         zuzena:
    #           mezua gaira gehitu da
		self.assertTrue(False)