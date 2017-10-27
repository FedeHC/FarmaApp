# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_script import Manager
from csv_db import DB
from formulario import Login
import validar


# Creando objetos flask:
app = Flask(__name__)
manager = Manager(app)
bs = Bootstrap(app)
db = DB("usuario_clave.csv")


# App:
app.config["BOOTSTRAP_SERVE_LOCAL"] = True 			# Para activar versión local de Bootstrap.
app.config["SECRET_KEY"] = "UnaClaveSecreta"		# Clave random para formularios con Flask-WTF.


# Funciones:

@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def inicio():
	""" Función que redirige a inicio.html o usuario.html según condiciones. """
	
	log = Login()					# Objeto de formulario Login.

	if log.validate_on_submit():	# Si se ha presionado el botón enviar de login...
		user, clave = db.chequear(log.usuario.data, log.clave.data)
		if user:
			if clave:
				session["user"] = log.usuario.data
				return redirect(url_for("usuario"))

			else:					# Si la clave no corresponde con ese usuario...
				mensaje = "Contraseña inválida para <b>{}</b>".format(log.usuario.data)
				return render_template("inicio.html", login=log, info=mensaje)

		else:						# Si el usuario no existe en la DB...
			mensaje = "<b>{}</b> no es un usuario registrado".format(log.usuario.data)
			return render_template("inicio.html", login=log, info=mensaje)

	# En caso de ingresar por primera vez:
	return render_template("inicio.html", login=log)


@app.route("/usuario")
def usuario():
	""" Función que redirige a usuario.html """

	# En caso de ingresar por primera vez:
	return render_template("usuario.html")


@app.route("/ProductosXCliente")
def pxc():
	""" Función que redirige a pxc.html """

	# En caso de ingresar por primera vez:
	return render_template("pxc.html")


@app.route("/ClientesXProducto")
def cxp():
	""" Función que redirige a cxp.html """

	# En caso de ingresar por primera vez:
	return render_template("cxp.html")


@app.route("/ProductosMasVendidos")
def pmv():
	""" Función que redirige a pmv.html """

	# En caso de ingresar por primera vez:
	return render_template("pmv.html")


@app.route("/ClientesMasGastaron")
def cmg():
	""" Función que redirige a cmg.html """

	# En caso de ingresar por primera vez:
	return render_template("cmg.html")


@app.route("/salir")
def salir():
	""" Función que desloguea usuario actual y redirige a inicio. """
	session.pop("user", None)
	flash("Usuario deslogueado")
	return redirect(url_for("inicio"))


@app.errorhandler(404)
def no_encontrado(e):
	""" Función que redirige a 404.html en caso de no encontrar la página solicitada. """
	return render_template("404.html"), 404


@app.errorhandler(500)
def error_servidor(e):
	""" Función que redirige a 500.html en caso de surgir algún error en el servidor. """
	return render_template("500.html"), 500


# Iniciando:
if __name__ == "__main__":
	manager.run()

# FIN