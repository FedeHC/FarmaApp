# -----------------------------------------------------------------------------
# Final de Paradigmas de Programación y Estructura de Datos
# (1° Año, 2° Cuatr. - 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_bootstrap import Bootstrap, StaticCDN
from flask_script import Manager
import formularios, consultas, db, guardar


# Creando objetos flask:
app = Flask(__name__)
manager = Manager(app)
bs = Bootstrap(app)


# Constantes con rutas y nombres de archivos:
RUTA = ""
ERROR = RUTA + "error.log"
ARC_CSV = RUTA + "csv/archivo.csv"
USER_CLAVE = RUTA + "csv/usuario_clave.csv"


# App.config:
app.config["SECRET_KEY"] = "UnaClaveSecreta"			# Clave random para formularios de Flask-WTF.
app.config["BOOTSTRAP_SERVE_LOCAL"] = True 				# Para activar versión local de Bootstrap.
app.config["BOOTSTRAP_QUERYSTRING_REVVING"] = False		# Para quitar el "?bootstrap=..." cuando se
														# buscan los archivos de bootstrap locales.

# App.extensions:
app.extensions['bootstrap']['cdns']['jquery'] = StaticCDN()	# Para poder usar archivo jQuery local.


# Funciones:
@app.route("/login", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def inicio():
	""" Función que lleva a inicio.html o usuario.html según condiciones. """
	
	# Si existe algún 'user' en sesión:
	if session.get("user"):
		return redirect(url_for("usuario"))

	# En caso de no haber usuario logueado, se prosigue:
	else:
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
					error = "clave inválida"
					return render_template("inicio.html",
											error=error,
											login=log)

			# Si el usuario no existe en la DB:
			else:
				error = "<b>{}</b> no es un usuario registrado".format(log.usuario.data)
				return render_template("inicio.html",
										error=error,
										login=log)

		# En caso de ingresar por primera vez:
		return render_template("inicio.html",
								login=log)


@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
	""" Función que lleva a registro.html, inicio.html o usuario.html según condiciones. """

	# Si existe algún 'user' en sesión:
	if session.get("user"):
		return redirect(url_for("usuario"))

	# En caso de no haber usuario logueado, se prosigue:
	else:
		registro = formularios.Registro()
		
		# Si se presiona el botón enviar:
		if registro.validate_on_submit():
			
			# Si los campos de claves son distintos entre si:
			if registro.clave.data != registro.repetir_clave.data:
				error = "Las claves ingresadas son distintas entre si."
				return render_template("registro.html",
										error=error,
										registro=registro)
			
			# Si ambas claves son iguales, se prosigue:
			else:
				bd = db.DB(USER_CLAVE)
				user, clave = bd.chequear(registro.usuario.data, registro.clave.data)
				
				# Si ya existe usuario:
				if user:
					error = "<b>{}</b> ya es un usuario registrado".format(registro.usuario.data)
					return render_template("registro.html",
											error=error,
											registro=registro)

				# En caso contrario, se registra y se redirecciona a inicio:
				registro_ok = bd.crear(registro.usuario.data, registro.clave.data)
				if registro_ok:
					flash("El usuario ha sido registrado con éxito")
					return redirect(url_for("inicio"))

				# Si surgió algún error durante el registro, se notifica:
				else:
					error = "Hubo un error al intentar registrarse en la DB."
					return render_template("registro.html",
											error=error,
											registro=registro)

		# En caso de ingresar por primera vez:
		return render_template("registro.html",
								registro=registro)


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
									usuario=True,
									resultados=resultados,
									nro_filas=nro_filas,
									cantidad=CANTIDAD)

		# En caso de que el CSV no se haya validado correctamente:
		else:
			error = "Hubo errores durante la validación del CSV (chequear log)"
			return render_template("usuario.html",
									usuario=True,
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
		exportar = formularios.Exportar()

		# Creando objeto consulta y obteniendo sugerencias:
		consulta = consultas.Consultas(ARC_CSV, ERROR)
		todos_clientes = consulta.listar_x("CLIENTE")

		# Si se presiona el botón de enviar:
		if busqueda.validate_on_submit() and busqueda.submit.data or exportar.validate_on_submit() and exportar.guardar.data:

			# Obteniendo palabra desde un StringField del formulario (si hay):
			if busqueda.buscar.data:
				pxc.palabra = busqueda.buscar.data.lower()

			# Obteniendo resultados:
			resultados, columnas = consulta.listar_x_en_y(pxc.palabra, "PRODUCTO", "CLIENTE")
			
			# Si hubo resultados:
			if len(resultados) > 1:

				# Si se presiona el botón de 'guardar resultados en csv':
				if exportar.validate_on_submit() and exportar.guardar.data:

					# Guardando resultados en CSV:
					titulo = "[Consulta: Productos x Cliente]"
					exportar = guardar.Exportar(RUTA, titulo, resultados)
					nombre_archivo = exportar.nombre_completo()

					if nombre_archivo:
						mensaje = "Los resultados fueron guardados en: <b>{}</b".format(nombre_archivo)
						return render_template("pxc.html",
												mensaje=mensaje,
												busqueda_pxc=busqueda,
												todos_clientes=todos_clientes)
					else:
						error = "Hubo un problema al intentar crear el archivo CSV."
						return render_template("pxc.html",
												error=error,
												busqueda_pxc=busqueda,
												todos_clientes=todos_clientes)

				else:
					return render_template("pxc.html",
											busqueda_pxc=busqueda,
											exportar=exportar,
											todos_clientes=todos_clientes,
											resultados=resultados,
											columnas=columnas)
			# Si NO hubo resultados: 
			else:
				error = "No hubo resultados con ese término"
				return render_template("pxc.html",
										error=error,
										busqueda_pxc=busqueda,
										todos_clientes=todos_clientes)					

		# Si no se envia aún ninguna búsqueda:
		return render_template("pxc.html",
								busqueda_pxc=busqueda,
								todos_clientes=todos_clientes)

	# Si NO hay 'user' en sesión:
	else:
		return redirect(url_for("inicio"))


@app.route("/productos", methods=["GET", "POST"])
def cxp():
	""" Función que lleva a cxp.html o inicio.html según determinadas condiciones. """

	# SI hay 'user' en sesión:
	if session.get("user"):
		busqueda = formularios.Busqueda()
		exportar = formularios.Exportar()

		# Creando objeto consulta y obteniendo sugerencias:
		consulta = consultas.Consultas(ARC_CSV, ERROR)
		todos_productos = consulta.listar_x("PRODUCTO")

		# Si se presiona el botón de enviar:
		if busqueda.validate_on_submit() and busqueda.submit.data or exportar.validate_on_submit() and exportar.guardar.data:

			
			# Obteniendo palabra desde un StringField del formulario (si hay):
			if busqueda.buscar.data:
				cxp.palabra = busqueda.buscar.data.lower()

			# Obteniendo resultados:
			resultados, columnas = consulta.listar_x_en_y(cxp.palabra, "CLIENTE", "PRODUCTO")

			# SI hubo resultados:
			if len(resultados) > 1:

				# Si se presiona el botón de 'guardar resultados en csv':
				if exportar.validate_on_submit() and exportar.guardar.data:

					# Guardando resultados en CSV:
					titulo = "[Consulta: Clientes x Producto]"
					exportar = guardar.Exportar(RUTA, titulo, resultados)
					nombre_archivo = exportar.nombre_completo()

					if nombre_archivo:
						mensaje = "Los resultados fueron guardados en: <b>{}</b".format(nombre_archivo)
						return render_template("cxp.html",
												mensaje=mensaje,
												busqueda_cxp=busqueda,
												todos_productos=todos_productos)
					else:
						error = "Hubo un problema al intentar crear el archivo CSV."
						return render_template("cxp.html",
												error=error,
												busqueda_cxp=busqueda,
												todos_productos=todos_productos)

				else:
					return render_template("cxp.html",
											busqueda_cxp=busqueda,
											exportar=exportar,
											todos_productos=todos_productos,
											resultados=resultados,
											columnas=columnas)

			# Si NO hubo resultados: 
			else:
				error = "No hubo resultados con ese término"
				return render_template("cxp.html",
										error=error,
										busqueda_cxp=busqueda,
										todos_productos=todos_productos)
		
		# Si NO se envia aún ninguna búsqueda:
		return render_template("cxp.html",
								busqueda_cxp=busqueda,
								todos_productos=todos_productos)

	# Si NO hay 'user' en sesión:
	else:
		return redirect(url_for("inicio"))


@app.route("/masvendidos", methods=["GET", "POST"])
def pmv():
	""" Función que lleva a pmv.html o inicio.html según si hay sesión abierta o no. """

	# SI hay 'user' en sesión:
	if session.get("user"):
		traer = formularios.Traer()
		exportar = formularios.Exportar()

		# Si se presiona el botón de enviar:
		if traer.validate_on_submit() and traer.submit.data or exportar.validate_on_submit() and exportar.guardar.data:

			# Obteniendo palabra desde un IntegerField del formulario (si hay datos):
			if traer.buscar.data:
				pmv.cantidad = traer.buscar.data

			# Creando objeto consulta y obteniendo resultados:
			consulta = consultas.Consultas(ARC_CSV, ERROR)
			resultados, columnas = consulta.listar_los_mas_x(pmv.cantidad, "PRODUCTO", "CANTIDAD")

			# Si se presiona el botón de 'guardar resultados en csv':
			if exportar.validate_on_submit() and exportar.guardar.data:

				# Guardando resultados en CSV:
				titulo = "[Consulta: Productos más vendidos]"
				exportar = guardar.Exportar(RUTA, titulo, resultados)
				nombre_archivo = exportar.nombre_completo()

				if nombre_archivo:
					mensaje = "Los resultados fueron guardados en: <b>{}</b".format(nombre_archivo)
					return render_template("pmv.html",
											mensaje=mensaje,
											traer_pmv=traer)
				else:
					error = "Hubo un problema al intentar crear el archivo CSV."
					return render_template("pmv.html",
											error=error,
											traer_pmv=traer)

			else:
				return render_template("pmv.html",
										traer_pmv=traer,
										exportar=exportar,
										resultados=resultados,
										columnas=columnas)

		# Si NO se envia aún ninguna búsqueda:
		return render_template("pmv.html",
								traer_pmv=traer)

	# Si NO hay 'user' en sesión:
	else:										
		return redirect(url_for("inicio"))


@app.route("/masgastaron", methods=["GET", "POST"])
def cmg():
	""" Función que lleva a cmg.html o inicio.html según si hay sesión abierta o no. """

	# SI hay 'user' en sesión:
	if session.get("user"):
		traer = formularios.Traer()
		exportar = formularios.Exportar()

		# Si se presiona el botón de enviar:
		if traer.validate_on_submit() and traer.submit.data or exportar.validate_on_submit() and exportar.guardar.data:

			# Obteniendo palabra desde un IntegerField del formulario (si hay datos):
			if traer.buscar.data:
				cmg.cantidad = traer.buscar.data

			# Creando objeto consulta y obteniendo resultados:
			consulta = consultas.Consultas(ARC_CSV, ERROR)
			resultados, columnas = consulta.listar_los_mas_x(cmg.cantidad, "CLIENTE", "PRECIO")

			# Si se presiona el botón de 'guardar resultados en csv':
			if exportar.validate_on_submit() and exportar.guardar.data:

				# Guardando resultados en CSV:
				titulo = "[Consulta: Clientes que más gastaron]"
				exportar = guardar.Exportar(RUTA, titulo, resultados)
				nombre_archivo = exportar.nombre_completo()

				if nombre_archivo:
					mensaje = "Los resultados fueron guardados en: <b>{}</b".format(nombre_archivo)
					return render_template("cmg.html",
											mensaje=mensaje,
											traer_cmg=traer)
				else:
					error = "Hubo un problema al intentar crear el archivo CSV."
					return render_template("cmg.html",
											error=error,
											traer_cmg=traer)

			else:
				return render_template("cmg.html",
										traer_cmg=traer,
										exportar=exportar,
										resultados=resultados,
										columnas=columnas)

		# Si NO se envia aún ninguna búsqueda:
		return render_template("cmg.html",
		 						traer_cmg=traer)

	# Si NO hay 'user' en sesión:
	else:										
		return redirect(url_for("inicio"))


@app.route("/clave", methods=["GET", "POST"])
def clave():
	""" Función que lleva a clave.html o inicio.html según condiciones. """

	# Si no existe algún 'user' en sesión, se redirige a inicio:
	if not session.get("user"):
		return redirect(url_for("inicio"))

	# En caso de haberlo, se prosigue:
	else:
		cambio = formularios.Cambio_Clave()

		# Si se presiona el botón enviar:
		if cambio.validate_on_submit():

			bd = db.DB(USER_CLAVE)
			user, clave = bd.chequear(session.get("user"), cambio.vieja_clave.data)

			# Si la vieja clave es la correcta, se prosigue:
			if clave:
				# Si las nuevas claves son ambas idénticas, entonces se procede a cambiar:
				if cambio.nueva_clave.data == cambio.confirmar_nueva_clave.data:

					borrar_ok = bd.borrar(session.get("user"), cambio.vieja_clave.data)
					agregar_ok = bd.crear(session.get("user"), cambio.nueva_clave.data)

					# Si la operación de cambiar ha sido exitosa:
					if borrar_ok and agregar_ok:
						mensaje = "La clave ha sido cambiada con éxito"
						return render_template("clave.html",
												mensaje=mensaje,
												cambio=cambio)
					else:
						error = "Hubo un error al intentar cambiar claves en DB."
						return render_template("clave.html",
												error=error,
												cambio=cambio)
				else:
					error = "La nuevas claves ingresadas son distintas entre si"
					return render_template("clave.html",
											error=error,
											cambio=cambio)

			# Si la clave no corresponde con ese usuario:
			else:
				error = "La clave actual es inválida"
				return render_template("clave.html",
										error=error,
										cambio=cambio)


		# En caso de ingresar por primera vez:
		return render_template("clave.html",
								cambio=cambio)


@app.route("/salir")
def salir():
	""" Función que desloguea al usuario actual y lleva a inicio.html """

	# SI hay 'user' en sesión:
	if session.get("user"):
		session.pop("user", None)
		flash("Usuario deslogueado")

	# Haya o no sesión abierta, se retorna a inicio.html:
	return redirect(url_for("inicio"))


@app.errorhandler(404)
def no_encontrado(e):
	""" Función que lleva a 404.html en caso de no encontrar la página solicitada. """
	return render_template("404.html"), 404


@app.errorhandler(500)
def error_servidor(e):
	""" Función que lleva a 500.html en caso de surgir algún error en el servidor. """
	return render_template("500.html"), 500


# Iniciando:
if __name__ == "__main__":
	manager.run()


# FIN