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
	titulua = request.values.get("titulua", "")

	if titulua:
		Liburua, nb_books = library.getLiburuak(titulua)
		return render_template('liburua.html', Liburua=Liburua)
	else:
		izenburua = request.values.get("izenburua", "")
		page = int(request.values.get("page", 1))
		Liburua, nb_books = library.getLiburuak(izenburua)
		total_pages = (nb_books // 6) + 1
		return render_template('catalogue.html', Liburua=Liburua, izenburua=izenburua, current_page=page,
							   total_pages=total_pages, max=max, min=min)

@app.route('/liburua')
def liburua():
	user = getActualUser()
	if user:
		titulua = request.values.get("titulua", "")
		#return f"titulua? {titulua}"
		if titulua:
			Liburua, nb_books = library.getLiburuak(titulua)
			#return f"liburua? {Liburua[0]}"
			liburuaErreserbatu(Liburua[0].id, user.username)
			return redirect('/erreserbak')
		else:
			return redirect("/catalogue")
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			return redirect('/login')
	return redirect("/catalogue")

@app.route('/erreserbak')
def erreserbak():
	user = getActualUser()

	if user:
		Erreserbak = erreserbakIkusi(user.username)
		Liburua = [liburuKopiaIkusi(e.liburuID) for e in Erreserbak]

		class Mezcla:
			def __init__(self, lib, erre):
				self.lib = lib
				self.erre = erre

		Info = [Mezcla(Liburua[e], Erreserbak[e]) for e in range(len(Erreserbak))]

		resp = render_template('erreserbak.html', Info=Info)
		id = request.values.get("id", "")
		if id:
			liburuaBueltatu(id, user.username)
			return redirect('/erreserbak')

	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = redirect('/login')
	return resp

@app.route('/foroak')
def foroak():
	izenburua = request.values.get("izenburua", "")
	page = int(request.values.get("page", 1))
	Foroa, nb_books = library.getForoak(izenburua)
	total_pages = (nb_books // 6) + 1
	return render_template('foroak.html', Foroa=Foroa, izenburua=izenburua, current_page=page,
	                       total_pages=total_pages, max=max, min=min)

@app.route('/libSortu')
def libSortu():
	user = getActualUser()
	if user:
		if user.administratzaileaDa:
			izena = request.values.get("izena", "")
			argazkia = request.values.get("argazkia", "")
			idazlea = request.values.get("idazlea", "")
			urtea = request.values.get("urtea", "")
			sinopsia = request.values.get("sinopsia", "")
			pdf = request.values.get("pdf", "")

			if izena and argazkia and idazlea and urtea and sinopsia and pdf:
				liburuBerriaGehitu(argazkia, izena, urtea, idazlea, sinopsia, pdf)
				return redirect('/perfila')

			atzera = request.values.get("atzera", "")

			if atzera:
				return redirect('/perfila')

			resp = render_template('libSortu.html')
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = redirect('/login')
	return resp

@app.route('/erabEzabatu')
def erabEzabatu():
	user = getActualUser()
	if user:
		if user.administratzaileaDa:
			erabIzena = request.values.get("erabIzena", "")
			if erabIzena:
				erabiltzaileaEzabatu(erabIzena)
				return redirect('/perfila')

			atzera = request.values.get("atzera", "")
			if atzera:
				return redirect('/perfila')

			resp = render_template('erabEzabatu.html')
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = redirect('/login')
	return resp

@app.route('/erabSortu',  methods=['GET', 'POST'])
def erabSortu():
	user = getActualUser()
	if user:
		if user.administratzaileaDa:
			izenabizen = request.values.get("izenabizen", "")
			argazkia = request.values.get("argazkia", "")
			nan = request.values.get("nan", "")
			telefonoa = request.values.get("telefonoa", "")
			helbidea = request.values.get("helbidea", "")
			posta = request.values.get("posta", "")
			erabIzena = request.values.get("erabIzena", "")
			pasahitza = request.values.get("pasahitza", "")
			admin = request.form.get("admin", "")

			if izenabizen and argazkia and nan and telefonoa and helbidea and posta and erabIzena and pasahitza:
				if admin:
					adminDa = "True"
				else:
					adminDa = "False"
				erabiltzaileBerriaSortu(erabIzena, izenabizen, pasahitza, nan, telefonoa, posta, helbidea, argazkia,
										adminDa)
				return redirect('/perfila')

			atzera = request.values.get("atzera", "")

			if atzera:
				return redirect('/perfila')

			resp = render_template('erabSortu.html')
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = redirect('/login')
	return resp

@app.route('/perfila')
def perfila():

	user = getActualUser()

	if user:
		erabSortu = request.values.get("erabSortu", "")
		erabEzabatu = request.values.get("erabEzabatu", "")
		libSortu = request.values.get("libSortu", "")
		erreserbak = request.values.get("erreserbak", "")

		if erabSortu:
			return redirect('/erabSortu')
		elif erabEzabatu:
			return redirect('/erabEzabatu')
		elif libSortu:
			return redirect('/libSortu')
		elif erreserbak:
			return redirect('/erreserbak')

		resp = render_template('perfila.html', user=user)

	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = redirect('/login')
	return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	erabiltzaileID = request.values.get("erabiltzaileID", "")
	password = request.values.get("password", "")
	user = library.getErabiltzaile(erabiltzaileID, password)
	if user:
		session = user.sortuSaioa()
		resp = redirect('/perfila')
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


def foroaBerriaSortu(fIzena, eIzena, deskribapena):
	LibraryController().foroaSortu(fIzena, eIzena, deskribapena)

def komentatuForoan(foroID, testua, erabiltzaileID):
	foroa = LibraryController().getForoa(foroID)
	if foroa is None:
		return
	foroa.gehituMezua(erabiltzaileID, testua)

def ikusiForoa(foroID):
	foroa = LibraryController().getForoa(foroID)
	if foroa is None:
		return
	foroa.getMezuak()

# LAGUNAK

def lagunEskaeraKudeatu(onartuDa, aErabiltzaileaID, bErabiltzaileaID):
	user = LibraryController().erabiltzaileBilatu(aErabiltzaileaID)
	if user is None:
		return
	user.eskaeraKudeatu(onartuDa, bErabiltzaileaID)

def lagunEskaeraBidali(igorleID, jasotzaileID):
	LibraryController().setLagunEskaera(igorleID, jasotzaileID)

# ERRESERBAK

def erreserbakIkusi(erabiltzaileID):
	return LibraryController().getErreserbak(erabiltzaileID)

def liburuaErreserbatu(liburuID, erabiltzaileID):
	liburua = LibraryController().getLiburua(liburuID)
	if liburua is None:
		return
	liburua.erreserbatu(erabiltzaileID)

# ERRESEINAK

def erreseinaEgin(erreseinaID, puntuazioa, testua):
	LibraryController().erreseinaEguneratu(erreseinaID,puntuazioa,testua)

def erreseinakIkusi(erabiltzaileID, liburuID):
	LibraryController().getErreseinak(erabiltzaileID, liburuID)

# ADMINISTRATZAILE FUNTZIOAK

def liburuBerriaGehitu(portada, izenburua, urtea, idazlea, sinopsia, PDF):
	LibraryController().liburuBerriaGehitu(portada, izenburua, urtea, idazlea, sinopsia, PDF)

def erabiltzaileBerriaSortu(eIzena, izenAbizenak, pasahitza, nan, tel, pElek, helb, argazkia, administratzaileaDa):
	LibraryController().erabiltzaileBerriaSortu(eIzena, izenAbizenak, pasahitza, nan, tel, pElek, helb, argazkia, administratzaileaDa)

def erabiltzaileaEzabatu(eIzena):
	LibraryController().erabiltzaileaEzabatu(eIzena)


# ERABILTZAILEAK

def erabiltzaileaBilatu(eIzena):
	LibraryController().erabiltzaileBilatu(eIzena)

# LIBURUAK

def liburuKatalogoanBilatu(hitzGako):
	LibraryController().getLiburuak(hitzGako)

def liburuaBueltatu(liburuID, erabiltzaileID):
	liburua = LibraryController().getLiburua(LibraryController().getLiburuKopiaID(liburuID))
	if liburua is None:
		return
	liburua.bueltatu(erabiltzaileID, liburuID)

def liburuaIkusi(liburuID):
	LibraryController().getLiburua(liburuID)

def liburuKopiaIkusi(liburuID):
	return LibraryController().getLiburuKopia(liburuID)
