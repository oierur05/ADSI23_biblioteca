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
		Liburua, nb_books = liburuKatalogoanBilatu(titulua)
		erreseinak = erreseinakIkusi(Liburua[0].id)
		return render_template('liburua.html', Liburua=Liburua[0], Erreseinak=erreseinak, bueltatu="False")
	else:
		izenburua = request.values.get("izenburua", "")
		page = int(request.values.get("page", 1))
		Liburua, nb_books = liburuKatalogoanBilatu(izenburua)
		total_pages = (nb_books // 6) + 1
		return render_template('catalogue.html', Liburua=Liburua, izenburua=izenburua, current_page=page,
							   total_pages=total_pages, max=max, min=min)

@app.route('/lagunak')
def lagunak():
	user = getActualUser()
	if user:

		Eskaerak = lagunEskaerakLortu(user.username)
		Lagunak = lagunakLortu(user.username)

		lagunIzena = request.values.get("lagunIzena", "")

		if lagunIzena:
			Bilatua = erabiltzaileaBilatu(lagunIzena)
			return render_template('lagunak.html', User=Bilatua, Eskaerak=Eskaerak, Lagunak=Lagunak)

		eskBidali = request.values.get("eskBidali", "")

		if eskBidali:
			if not lagunakDira(user.username, eskBidali) and user.username != eskBidali:
				lagunEskaeraBidali(user.username, eskBidali)


		onartu = request.values.get("onartu", "")

		if onartu:
			lagunEskaeraBidali(user.username, onartu)
			lagunEskaeraKudeatu(True, user.username, onartu)
			Eskaerak = lagunEskaerakLortu(user.username)
			Lagunak = lagunakLortu(user.username)
			return render_template('lagunak.html', User=None, Eskaerak=Eskaerak, Lagunak=Lagunak)

		ezeztatu = request.values.get("ezeztatu", "")

		if ezeztatu:
			lagunEskaeraKudeatu(False, user.username, ezeztatu)
			Eskaerak = lagunEskaerakLortu(user.username)
			Lagunak = lagunakLortu(user.username)
			return render_template('lagunak.html', User=None, Eskaerak=Eskaerak, Lagunak=Lagunak)

		bisitatu = request.values.get("bisitatu", "")

		if bisitatu:
			laguna = erabiltzaileaBilatu(bisitatu)
			lagunarenLagunak = lagunakLortu(bisitatu)
			Erreserbak = erreserbakIkusi(bisitatu)
			Liburua = [liburuKopiaIkusi(e.liburuID) for e in Erreserbak]

			class Mezcla:
				def __init__(self, lib, erre):
					self.lib = lib
					self.erre = erre

			Info = [Mezcla(Liburua[e], Erreserbak[e]) for e in range(len(Erreserbak))]

			Erreseinak = erreseinakIkusiErabiltzaileko(bisitatu)
			ErreseinaLiburua = [liburuaIkusi(e.libID) for e in Erreseinak]

			InfoErreseinak = [Mezcla(ErreseinaLiburua[e], Erreseinak[e]) for e in range(len(Erreseinak))]

			irakurritakoLiburuak = [liburuaIkusi(e.libID) for e in Erreseinak]

			return render_template('perfilabisitatu.html', user=laguna, Lagunak=lagunarenLagunak, Info=Info, Liburua=irakurritakoLiburuak, Erreseinak=InfoErreseinak)

		return render_template('lagunak.html', User=None, Eskaerak=Eskaerak, Lagunak=Lagunak)

	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			return redirect('/login')

	return redirect("/catalogue")

@app.route('/liburua')
def liburua():
	user = getActualUser()
	if user:
		titulua = request.values.get("titulua", "")
		#return f"titulua? {titulua}"
		if titulua:
			Liburua, nb_books = liburuKatalogoanBilatu(titulua)
			#return f"liburua? {Liburua[0]}"
			liburuaErreserbatu(Liburua[0].id, user.username)
			return redirect('/erreserbak')

		like = request.values.get("like", "")

		if like:
			erreseinaLikeGehitu(user.username, like)
			Liburua = liburuaIkusi(like)
			erreseinak = erreseinakIkusi(like)
			return render_template('liburua.html', Liburua=Liburua, Erreseinak=erreseinak, bueltatu="False")

		erreseinaegin = request.values.get("erreseinaegin", "")

		if erreseinaegin:
			testua = request.values.get("testua", "")
			balorazioa = request.values.get("balorazioa", "")
			if int(balorazioa) > 10:
				balorazioa = "10"
			elif int(balorazioa) < 0:
				balorazioa = "0"
			liburuid = request.values.get("liburuid", "")
			erreseinaEgin(user.username, liburuid, balorazioa, testua)
			Liburua = liburuaIkusi(liburuid)
			erreseinak = erreseinakIkusi(liburuid)
			return render_template('liburua.html', Liburua=Liburua, Erreseinak=erreseinak, bueltatu="False")

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
			lib = liburuKopiaIkusi(id)
			erreseinak = erreseinakIkusi(lib.id)
			erreseinaEgin(user.username, lib.id, "egin gabe", "")
			return render_template('liburua.html', Liburua=lib, Erreseinak=erreseinak, bueltatu="True")

	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = redirect('/login')
	return resp

@app.route('/irakurritakoak')
def irakurritakoak():
	user = getActualUser()

	if user:
		id = request.values.get("id", "")
		if id:
			lib = liburuaIkusi(id)
			erreseinak = erreseinakIkusi(id)
			erreseinaEgin(user.username, id, "egin gabe", "")
			return render_template('liburua.html', Liburua=lib, Erreseinak=erreseinak, bueltatu="True")

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
	Foroa, nb_books = foroKatalogoanForoBilatu(izenburua)
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
		irakurritakoak = request.values.get("irakurritakoak", "")
		lagunak = request.values.get("lagunak", "")

		if erabSortu:
			return redirect('/erabSortu')
		elif erabEzabatu:
			return redirect('/erabEzabatu')
		elif libSortu:
			return redirect('/libSortu')
		elif erreserbak:
			return redirect('/erreserbak')
		elif irakurritakoak:
			Erreseinak = erreseinakIkusiErabiltzaileko(user.username)
			Liburua = [liburuaIkusi(e.libID) for e in Erreseinak]
			return render_template('irakurritakoak.html', Liburua=Liburua)
		elif lagunak:
			return redirect('/lagunak')

		id = request.values.get("id", "")
		if id:
			lib = liburuaIkusi(id)
			erreseinak = erreseinakIkusi(id)
			erreseinaEgin(user.username, id, "egin gabe", "")
			return render_template('liburua.html', Liburua=lib, Erreseinak=erreseinak, bueltatu="True")

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
	return LibraryController().getForoak(hitzGako)

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

def lagunEskaeraKudeatu(onartuDa, igorleID, jasotzaileID):
	user = LibraryController().erabiltzaileBilatu(igorleID)
	if user is None:
		return
	user.eskaeraKudeatu(onartuDa, jasotzaileID)

def lagunEskaeraBidali(igorleID, jasotzaileID):
	LibraryController().setLagunEskaera(igorleID, jasotzaileID)

def lagunEskaerakLortu(jasotzaileID):
	return LibraryController().getLagunEskaerak(jasotzaileID)

def lagunakLortu(jasotzaileID):
	return LibraryController().getLagunak(jasotzaileID)

def lagunakDira(igorleID, jasotzaileID):
	return LibraryController().getLagunakDira(igorleID, jasotzaileID)

# ERRESERBAK

def erreserbakIkusi(erabiltzaileID):
	return LibraryController().getErreserbak(erabiltzaileID)

def liburuaErreserbatu(liburuID, erabiltzaileID):
	liburua = LibraryController().getLiburua(liburuID)
	if liburua is None:
		return
	liburua.erreserbatu(erabiltzaileID)

# ERRESEINAK

def erreseinaEgin(erreseinaID, liburuID, puntuazioa, testua):
	LibraryController().erreseinaEguneratu(erreseinaID, liburuID, puntuazioa, testua)

def erreseinakIkusi(liburuID):
	return LibraryController().getErreseinak(liburuID)

def erreseinakIkusiErabiltzaileko(erabiltzaileizena):
	return LibraryController().getErreseinakErabiltzaileko(erabiltzaileizena)

def erreseinaLikeGehitu(erabiltzaileID, liburuID):
	LibraryController().erreseinaLikeGehitu(erabiltzaileID, liburuID)

# ADMINISTRATZAILE FUNTZIOAK

def liburuBerriaGehitu(portada, izenburua, urtea, idazlea, sinopsia, PDF):
	LibraryController().liburuBerriaGehitu(portada, izenburua, urtea, idazlea, sinopsia, PDF)

def erabiltzaileBerriaSortu(eIzena, izenAbizenak, pasahitza, nan, tel, pElek, helb, argazkia, administratzaileaDa):
	LibraryController().erabiltzaileBerriaSortu(eIzena, izenAbizenak, pasahitza, nan, tel, pElek, helb, argazkia, administratzaileaDa)

def erabiltzaileaEzabatu(eIzena):
	LibraryController().erabiltzaileaEzabatu(eIzena)


# ERABILTZAILEAK

def erabiltzaileaBilatu(eIzena):
	return LibraryController().erabiltzaileBilatu(eIzena)

# LIBURUAK

def liburuKatalogoanBilatu(hitzGako):
	return LibraryController().getLiburuak(hitzGako)

def liburuaBueltatu(liburuID, erabiltzaileID):
	liburua = LibraryController().getLiburua(LibraryController().getLiburuKopiaID(liburuID))
	if liburua is None:
		return
	liburua.bueltatu(erabiltzaileID, liburuID)

def liburuaIkusi(liburuID):
	return LibraryController().getLiburua(liburuID)

def liburuKopiaIkusi(liburuID):
	return LibraryController().getLiburuKopia(liburuID)
