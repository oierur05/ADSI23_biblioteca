from model import User
from .LibraryController import LibraryController
from flask import Flask, render_template, request, make_response, redirect
from model.Connection import Connection

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')
db = Connection()


library = LibraryController()


@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = library.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token


@app.after_request
def add_cookies(response):
	if 'user' in dir(request) and request.user and request.user.token:
		session = request.user.validate_session(request.user.token)
		response.set_cookie('token', session.hash)
		response.set_cookie('time', str(session.time))
	return response


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/catalogue')
def catalogue():
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(title=title, author=author, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('catalogue.html', books=books, title=title, author=author, current_page=page,
	                       total_pages=total_pages, max=max, min=min)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = library.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp

def getActualUser():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			user = library.get_user_cookies(token, float(time))
			if user:
				return user


# FOROAK

def foroKatalogoanForoBilatu(hitzGako):
	LibraryController().getForoak(hitzGako)
	## ESTO HABRIA QUE PONERLO EN EL LIBRARYCONTROLLER
	#emaitzak = db.select("SELECT * from FOROA WHERE foroID LIKE ? OR erabiltzaileIzena LIKE ? OR izena LIKE ? OR deskribapena LIKE ? OR sorreraData LIKE ?", (
	#	'%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',))
	#return emaitzak.fetchall()


def foroaBerriaSortu(fIzena, eIzena, deskribapena):
	# HAY QUE HACERLO
	return

def komentatuForoan(testua, erabiltzaileID):
	# HAY QUE HACERLO
	return

def getForoa(foroID):
	# HAY QUE HACERLO
	return

# LAGUNAK

def lagunEskaeraKudeatu(onartuDa, aErabiltzaileaID, bErabiltzaileaID):
	user = LibraryController().erabiltzaileBilatu(aErabiltzaileaID)
	user.eskaeraKudeatu(onartuDa, bErabiltzaileaID)

def lagunEskaeraBidali(igorleID, jasotzaileID):
	LibraryController().setLagunEskaera(igorleID, jasotzaileID)

# ERRESERBAK

def erreserbakIkusi(erabiltzaileID):
	LibraryController().getErreserbak(erabiltzaileID)

def liburuaErreserbatu(liburuID, erabiltzaileID):
	liburua = LibraryController().getLiburua(liburuID)
	liburua.erreserbatu(erabiltzaileID)
# ERRESEINAK

def erreseinaEgin(erreseinaID, puntuazioa, testua):
	LibraryController().erreseinaEguneratu(erreseinaID,puntuazioa,testua)

def erreseinakIkusi(erabiltzaileID):
	LibraryController().getErreseinak(erabiltzaileID)

# ADMINISTRATZAILE FUNTZIOAK

def liburuBerriaGehitu(portada, izenburua, urtea, idazlea, sinopsia, PDF):
	LibraryController().liburuBerriaGehitu(portada, izenburua, urtea, idazlea, sinopsia, PDF)

def erabiltzaileBerriaSortu(eIzena, izenAbizenak, pasahitza, nan, tel, pElek, helb, argazkia, administratzaileaDa):
	LibraryController().erabiltzaileBerriaSortu(eIzena, izenAbizenak, pasahitza, nan,
												tel, pElek, helb, argazkia, administratzaileaDa)

def erabiltzaileaEzabatu(eIzena):
	LibraryController().erabiltzaileaEzabatu(eIzena)

# ERABILTZAILEAK

def erabiltzaileaBilatu(eIzena):
	LibraryController().erabiltzaileBilatu(eIzena)
	# ESTO HABRIA QUE PONERLO EN EL LIBRARYCONTROLLER
	#emaitzak = db.select("SELECT * from User WHERE izena LIKE ?", (
	#	eIzena + '%',))
	#return emaitzak.fetchall()

# LIBURUAK

def liburuKatalogoanBilatu(hitzGako):
	LibraryController().getLiburuak(hitzGako)
	# ESTO HABRIA QUE PONERLO EN EL LIBRARYCONTROLLER
	#emaitzak = db.select("SELECT * from BOOK WHERE liburuID LIKE ? OR izenburua LIKE ? OR urtea LIKE ? OR idazlea LIKE ? OR sinopsia LIKE ?", (
	#	'%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%', '%' + hitzGako + '%',))
	#return emaitzak.fetchall()

def liburuaBueltatu(liburuID, erabiltzaileID):
	liburua = LibraryController().getLiburua(liburuID)
	liburua.bueltatu(erabiltzaileID)

def liburuaIkusi(liburuID):
	LibraryController().getLiburua(liburuID)