# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_script import Manager
import formularios, consultas, db


# Creando objetos flask:
app = Flask(__name__)
manager = Manager(app)
bs = Bootstrap(app)


# Constantes con nombres y rutas de archivos:
RUTA = ""
ARC_CSV = RUTA + "archivo.csv"
ERROR = RUTA + "error.log"
USER_CLAVE = RUTA + "usuario_clave.csv"


# App.config:
app.config["SECRET_KEY"] = "UnaClaveSecreta"			# Clave random para formularios de Flask-WTF.
app.config["BOOTSTRAP_SERVE_LOCAL"] = True 				# Para activar versión local de Bootstrap.
app.config["BOOTSTRAP_QUERYSTRING_REVVING"] = False		# Para quitar el "?bootstrap=..." cuando se
														# buscan los archivos de bootstrap locales.

# Funciones:
@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def inicio():
	""" Función que lleva a inicio.html o usuario.html según condiciones. """
	
	log = formularios.Login()
	
	# Si se presiona el botón enviar:
	if log.validate_on_submit():

		bd = db.DB(USER_CLAVE)
		user, clave = bd.chequear(log.usuario.data, log.clave.data)
		if user:
			if clave:
				session["user"] = log.usuario.data
				return redirect(url_for("usuario"))

			# Si la clave no corresponde con ese usuario:
			else:
				error = "Contraseña inválida para <b>{}</b>".format(log.usuario.data)
				return render_template("inicio.html",
										error=error,
										login=log)

		# Si el usuario no existe en la DB:
		else:
			error = "<b>{}</b> no es un usuario registrado".format(log.usuario.data)
			return render_template("inicio.html",
									error=error,
									login=log)


	# Si existe algún 'user' en session:
	if session.get("user"):
		return redirect(url_for("usuario"))

	# En caso de ingresar por primera vez:
	return render_template("inicio.html",
							login=log)


@app.route("/usuario", methods=["GET", "POST"])
def usuario():
	""" Función que lleva a usuario.html o inicio.html según condición. """

	# SI hay 'user' en sesión:
	if session.get("user"):

		# Creando objeto consulta:
		consulta = consultas.Consultas(ARC_CSV, ERROR)

		# Chequeando que validación del CSV haya sido correcta:
		if consulta.csv.ok:
			CANTIDAD=5
			resultados, nro_filas = consulta.ultimos_resultados(CANTIDAD)

			return render_template("usuario.html",
									resultados=resultados,
									nro_filas=nro_filas,
									cantidad=CANTIDAD)

		# En caso de que el CSV no se haya validado correctamente:
		else:
			error = "Hubo errores durante la validación del CSV"
			return render_template("usuario.html",
									error=error,
									mensajes_error=consulta.csv.mensajes_error)
	# Si NO hay 'user' en sesión:
	else:
		return redirect(url_for("inicio"))


@app.route("/clientes", methods=["GET", "POST"])
def pxc():
	""" Función que lleva a pxc.html o inicio.html según determinadas condiciones. """

	# SI hay 'user' en sesión:
	if session.get("user"):
		busqueda = formularios.Busqueda()

		# Si se presiona el botón 'enviar':
		if busqueda.validate_on_submit():

			# Obteniendo palabra desde un StringField del formulario:
			palabra = busqueda.buscar.data.lower()

			# Creando objeto consulta y obteniendo resultados:
			consulta = consultas.Consultas(ARC_CSV, ERROR)
			resultados, columnas = consulta.listar_x_en_y(palabra, "PRODUCTO", "CLIENTE")
			
			# Si hubo resultados:
			if len(resultados) > 1:
				return render_template("pxc.html",
										busqueda=busqueda,
										resultados=resultados,
										columnas=columnas)
			else:
				error = "No hubo resultados con ese término"
				return render_template("pxc.html",
										busqueda=busqueda,
										error=error)					

		# Si no se envia aún ninguna búsqueda:
		return render_template("pxc.html",
								busqueda=busqueda)

	# Si NO hay 'user' en sesión:
	else:
		return redirect(url_for("inicio"))


@app.route("/productos", methods=["GET", "POST"])
def cxp():
	""" Función que lleva a cxp.html o inicio.html según determinadas condiciones. """

	# SI hay 'user' en sesión:
	if session.get("user"):
		busqueda = formularios.Busqueda()

		# Si se presiona el botón 'enviar':
		if busqueda.validate_on_submit():
			
			# Obteniendo palabra desde un StringField del formulario:
			palabra = busqueda.buscar.data.lower()
			
			# Creando objeto consulta y obteniendo resultados:
			consulta = consultas.Consultas(ARC_CSV, ERROR)
			resultados, columnas = consulta.listar_x_en_y(palabra, "CLIENTE", "PRODUCTO")

			# SI hubo resultados:
			if len(resultados) > 1:
				return render_template("cxp.html",
										busqueda=busqueda,
										resultados=resultados,
										columnas=columnas)
			# Si NO hubo resultados:
			else:
				error = "No hubo resultados con ese término"
				return render_template("cxp.html",
										busqueda=busqueda,
										error=error)
		
		# Si NO se envia aún ninguna búsqueda:
		return render_template("cxp.html",
								busqueda=busqueda)

	# Si NO hay 'user' en sesión:
	else:
		return redirect(url_for("inicio"))


@app.route("/masvendidos", methods=["GET", "POST"])
def pmv():
	""" Función que lleva a pmv.html o inicio.html según si hay sesión abierta o no. """

	# SI hay 'user' en sesión:
	if session.get("user"):
		traer = formularios.Traer()

		# Si se presiona el botón 'enviar':
		if traer.validate_on_submit():

			# Obteniendo palabra desde un IntegerField del formulario:
			cantidad = traer.buscar.data

			# Creando objeto consulta y obteniendo resultados:
			consulta = consultas.Consultas(ARC_CSV, ERROR)
			resultados, columnas = consulta.listar_los_mas_x(cantidad, "PRODUCTO", "CANTIDAD")

			return render_template("pmv.html",
									traer=traer,
									resultados=resultados,
									columnas=columnas)

		# Si NO se envia aún ninguna búsqueda:
		return render_template("pmv.html",
		 						traer=traer)

	# Si NO hay 'user' en sesión:
	else:										
		return redirect(url_for("inicio"))


@app.route("/masgastaron", methods=["GET", "POST"])
def cmg():
	""" Función que lleva a cmg.html o inicio.html según si hay sesión abierta o no. """

	# SI hay 'user' en sesión:
	if session.get("user"):
		traer = formularios.Traer()

		# Si se presiona el botón 'enviar':
		if traer.validate_on_submit():

			# Obteniendo palabra desde un IntegerField del formulario:
			cantidad = traer.buscar.data

			# Creando objeto consulta y obteniendo resultados:
			consulta = consultas.Consultas(ARC_CSV, ERROR)
			resultados, columnas = consulta.listar_los_mas_x(cantidad, "CLIENTE", "PRECIO")

			return render_template("cmg.html",
									traer=traer,
									resultados=resultados,
									columnas=columnas)

		# Si NO se envia aún ninguna búsqueda:
		return render_template("cmg.html",
		 						traer=traer)

	# Si NO hay 'user' en sesión:
	else:										
		return redirect(url_for("inicio"))


@app.route("/salir")
def salir():
	""" Función que desloguea al usuario actual y redirige a inicio. """

	# SI hay 'user' en sesión:
	if session.get("user"):
		session.pop("user", None)
		flash("Usuario deslogueado")

	# Haya o no sesión abierta, se retorna a inicio.html:
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