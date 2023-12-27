class Erreseina:
   def __init__(self, erreseinaId, erabiltzaileIzena, puntuazioa, testua, likeKopurua):
       self.erreseinaId = erreseinaId
       self.erabiltzaileIzena = erabiltzaileIzena
       self.puntuazioa = puntuazioa
       self.testua = testua
       self.likeKopurua = likeKopurua


   def __str__(self):
       return f"{self.erreseinaId}"