import hashlib
import sqlite3
import json
import os


ruta_base_de_datos = os.path.join("..", "datos.db")


salt = "library"


con = sqlite3.connect(ruta_base_de_datos)
cur = con.cursor()


### Create tables
cur.execute("""
	CREATE TABLE IF NOT EXISTS Erabiltzailea(
		erabiltzaileizena VARCHAR(15) PRIMARY KEY,
   		izenabizenak VARCHAR(40),
   		pasahitza VARCHAR(20),
   		NAN VARCHAR(10), --CON GUION INCLUSIVE ;)
   		telefonoa INT,
   		postaelektronikoa VARCHAR(35),
   		helbidea VARCHAR(30),
   		argazkia VARCHAR(200),
   		administratzaileada BOOLEAN
	)
""")

#cur.execute("""DELETE FROM Erreseina WHERE erabiltzaileizena = 'juanbelio'""")
#con.commit()

cur.execute("""
	CREATE TABLE IF NOT EXISTS Laguna(
   		erabiltzaile1 VARCHAR(15),
   		erabiltzaile2 VARCHAR(15),
   		onartua BOOLEAN,
   		PRIMARY KEY (erabiltzaile1,erabiltzaile2),
   		FOREIGN KEY (erabiltzaile1) REFERENCES erabiltzailea(erabiltzaileizena),
   		FOREIGN KEY (erabiltzaile2) REFERENCES erabiltzailea(erabiltzaileizena)
	)
""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS Foroa(
		id INT PRIMARY KEY,
   		erabiltzaileizena VARCHAR(15),
   		izena VARCHAR(30),
   		deskribapena VARCHAR (100),
   		sorreraData DATE, --'2023-01-01'
   		FOREIGN KEY (erabiltzaileizena) REFERENCES erabiltzailea(erabiltzaileizena)
	)
""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS Erreseina(
		erabiltzaileizena VARCHAR(15),
   		liburuid INT,
   		puntuazioa INT,
   		testua VARCHAR(150),
   		likekopurua INT,
   		PRIMARY KEY (erabiltzaileizena,liburuid),
   		FOREIGN KEY (erabiltzaileizena) REFERENCES erabiltzailea(erabiltzaileizena),
   		FOREIGN KEY (liburuid) REFERENCES liburua(liburuid)
	)
""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS Saioa(
		hash VARCHAR(200),
   		erabiltzaileizena VARCHAR(15),
   		data DATETIME, --'2023-01-01 15:30:00'
   		PRIMARY KEY (hash,erabiltzaileizena),
   		FOREIGN KEY (erabiltzaileizena) REFERENCES erabiltzailea(erabiltzaileizena)
	)
""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS Data(
		data DATETIME PRIMARY KEY
	)
""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS Liburua(
		liburuid INT PRIMARY KEY,
 		portada VARCHAR(200),
 		izenburua VARCHAR(30),
 		urtea INT,
 		idazlea VARCHAR(30),
 		sinopsia VARCHAR(400),
 		PDF VARCHAR(200)
	)
""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS Kopiafisikoa(
		kopiaid INT PRIMARY KEY,
 		liburuid INT,
 		FOREIGN KEY (liburuid) REFERENCES liburua(liburuid)
	)
""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS Erreserba(
		kopiafisikoid INT,
   		erabiltzaileizena VARCHAR(15),
   		hasieradata DATETIME,
   		bukaeradata DATETIME,
   		PRIMARY KEY (kopiafisikoid,erabiltzaileizena,hasieradata),
   		FOREIGN KEY (erabiltzaileizena) REFERENCES erabiltzailea(erabiltzaileizena),
   		FOREIGN KEY (hasieradata) REFERENCES data(data),
   		FOREIGN KEY (kopiafisikoid) REFERENCES kopiafisikoa(kopiaid)
	)
""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS Mezua(
		erabiltzaileizena VARCHAR(15),
   		foroid INT,
   		data DATETIME,
   		testua VARCHAR (200),
   		PRIMARY KEY (erabiltzaileizena,foroid,data),
   		FOREIGN KEY (erabiltzaileizena) REFERENCES erabiltzailea(erabiltzaileizena),
   		FOREIGN KEY (foroid) REFERENCES foroa(id),
   		FOREIGN KEY (data) REFERENCES data(data)
	)
""")

#### Insert books

ruta_libros = os.path.join("..", "liburuak.tsv")
with open(ruta_libros, 'r') as f:
	libros = [x.split("\t") for x in f.readlines()]

for id, urtea, pdf, author, title, cover, description in libros:

	cur.execute("INSERT INTO Liburua VALUES (?, ?, ?, ?, ?, ?, ?)",
		            (id,cover, title, urtea, author, description.strip(),pdf))

	con.commit()

### Insert foroak

ruta_foros = os.path.join("..", "foroak.tsv")
with open(ruta_foros, 'r') as f:
	foros = [x.split("\t") for x in f.readlines()]

for id, erabiltzaileIzena, izena, desk, data in foros:

	cur.execute("INSERT INTO Foroa VALUES (?, ?, ?, ?, ?)",
		            (id, erabiltzaileIzena, izena, desk, data))

	con.commit()

### Insert kopiak

ruta_copias = os.path.join("..", "kopiafisikoa.tsv")
with open(ruta_copias, 'r') as f:
	copias = [x.split("\t") for x in f.readlines()]

for idKopia, idLib in copias:

	cur.execute("INSERT INTO Kopiafisikoa VALUES (?, ?)",
		            (idKopia,idLib))

	con.commit()




### Insert users

ruta_usuarios = os.path.join("..", "usuarios.json")
with open(ruta_usuarios, 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['pasahitza'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO Erabiltzailea VALUES ('{user['erabiltzaileizena']}', '{user['izenabizenak']}', '{dataBase_password}', '{user['NAN']}', '{user['telefonoa']}', '{user['postaelektronikoa']}', '{user['helbidea']}', '{user['argazkia']}', '{user['administratzaileada']}')""")
	con.commit()


