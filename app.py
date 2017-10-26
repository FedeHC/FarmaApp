from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_script import Manager
from csv_db import DB
from formulario import Login


# Iniciando:
app = Flask(__name__)
app.config["SECRET_KEY"] = "UnaClaveSecreta"
manager = Manager(app)
bs = Bootstrap(app)
db = DB('usuario_clave.csv')


@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def inicio():
	""" Función que redirige a inicio.html o usuario.html según condiciones. """
	
	log = Login()					# Objeto de formulario Login.

	if log.validate_on_submit():	# Si se ha presionado el botón enviar de login...
		user, clave = db.chequear(log.usuario.data, log.clave.data)
		if user:
			if clave:
				session['user'] = log.usuario.data
				return render_template("usuario.html")

			else:					# Si la clave no corresponde con ese usuario...
				mensaje = "Contraseña inválida para <b>{}</b>".format(log.usuario.data)
				return render_template("inicio.html", login=log, info=mensaje)

		else:						# Si el usuario no existe en la DB...
			mensaje = "<b>{}</b> no es un usuario registrado".format(log.usuario.data)
			return render_template("inicio.html", login=log, info=mensaje)

	# En caso de ingresar por primera vez:
	return render_template("inicio.html", login=log)


@app.route("/salir")
def salir():
	""" Función que desloguea usuario actual y redirige a inicio. """
	session.pop('user', None)			# Eliminando al usuario de la sesión.
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
	# app.run(debug=True)
	manager.run()

# FIN