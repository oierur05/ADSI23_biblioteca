import hashlib
import sqlite3
import json

salt = "library"


con = sqlite3.connect("datos.db")
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

### Insert users
with open('usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['pasahitza'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO Erabiltzailea VALUES ('{user['erabiltzaileizena']}', '{user['izenabizenak']}', '{user['postaelektronikoa']}', '{dataBase_password}')""")
	con.commit()


#### Insert books
with open('libros.tsv', 'r') as f:
	libros = [x.split("\t") for x in f.readlines()]

for author, title, cover, description in libros:

	cur.execute("INSERT INTO Liburua VALUES (NULL, ?, ?, ?, ?, ?, ?)",
		            (cover,title, None, author, description.strip(),None))

	con.commit()



