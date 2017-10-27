# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

# Constantes:
LOG = "error.log"
ARCHIVO = "archivo.csv"

# Clases:

class MiExcepcion(Exception):
	""" Clase de excepcion personalizada para cuando se busca lanzar un error a partir de
	un archivo CSV leido (según ejercicio). """

	# Constructor:
	def __init__(self, mensajes_error):
		self.mensajes_error = mensajes_error


class Csv():
	""" La clase que contendrá todos los métodos para validar el CSV (según ejercicio). """
	
	def __init__(self, archivo_csv=ARCHIVO):
		""" Constructor de la clase. """

		self.mensajes_error = []		# Lista de errores que contendrá 3 campos:
										# 1) El tipo de campo en el que surgió el error.
										# 2) El N° de linea con el error.
										# 3) El mensaje de error en cuestión.

		# El método que realizará todos los pasos para la verificación del CSV:
		self.programa(archivo_csv)


	def programa(self, archivo_csv):
		""" Método que inicia la verificación de un CSV pasado como argumento. """

		# Creando error.log desde cero (en caso de que exista contenido previo):
		with open("error.log", "w") as log:
			log.write("")

		self.nombre = archivo_csv
		archivo, csv = self.abrir_csv()

		if archivo:				# Si no hubo problemas al abrir...
			primera_fila = self.obtener_primera_fila(csv, archivo)

			self.chequear(self.campos, primera_fila)
			self.chequear(self.codigos, primera_fila["codigo"])
			self.chequear(self.cantidades, primera_fila["cantidad"])
			self.chequear(self.precios, primera_fila["precio"])

		return 0


	def abrir_csv(self):
		""" Método que abre un CSV a partir de un nombre pasado como argumento.
		
			- Devuelve los objetos "open()" y "csv.reader()" si hay éxito.
			- Devuelve dos "None" en caso contrario. """

		import csv

		try:
			archivo = open(self.nombre, newline="")
			csv_abierto = csv.reader(archivo, delimiter=",", quoting=csv.QUOTE_NONE)
			
			return archivo, csv_abierto

		except FileNotFoundError:
			self.mensajes.append("ERROR: No se encontró el archivo \"{}\".".format(self.nombre))
			return None, None

		except PermissionError:
			self.mensajes.append("ERROR: No hay permisos para abrir el archivo \"{}\".".format(self.nombre))
			return None, None


	def obtener_primera_fila(self, csv_abierto, archivo):
		""" Método que obtiene la 1ra fila de un archivo CSV previamente abierto.
			
			- Devuelve un diccionario con los campos y sus valores numéricos corresp. """

		# Diccionario donde se guardará la ubicación de cada campo:
		campos = {"codigo": 0, "cliente": 0, "producto": 0, "cantidad": 0, "precio": 0}

		for c, fila in enumerate(csv_abierto):
			if c == 0:  										# Si es la 1ra fila...
				for valor, registro in enumerate(fila):
					if registro.upper().strip() == "CODIGO":
						campos["codigo"] = valor
					if registro.upper().strip() == "CLIENTE":
						campos["cliente"] = valor
					if registro.upper().strip() == "PRODUCTO":
						campos["producto"] = valor
					if registro.upper().strip() == "CANTIDAD":
						campos["cantidad"] = valor
					if registro.upper().strip() == "PRECIO":
						campos["precio"] = valor
			else:  												# Si son las otras filas...
				break

		# Cerramos el archivo y retornamos los campos obtenidos:
		archivo.close()
		return campos


	def chequear(self, funcion, nro_campo):
		""" Método que ejecuta otra función a partir de un campo y objeto CSV recibidos
		como parámetros.

			- Devuelve True si NO hubo errores.
			- Devuelve False SI en cambio hubo errores."""

		try:
			# Abrimos el archivo y el csv:
			archivo, csv_abierto = self.abrir_csv()

			# Se llama a la función recibida como parámetro:
			errores = funcion(csv_abierto, nro_campo)
			
			# Si recibimos mensajes de error, levantamos "MiExcepción":
			if errores:
				raise MiExcepcion(self.mensajes_error)
			
			archivo.close()
			return True

		except MiExcepcion as e:
			with open("error.log", "w") as log:
				for linea in e.mensajes_error:
					log.write("[Linea " + str(linea[1]) + "] " + linea[2] + "\n")

			return False


	def campos(self, csv_abierto, primera_fila):
		""" Método que chequea la cantidad de campos de todas las filas de un archivo CSV."""
	
		cant_campos = len(primera_fila)
		for c, fila in enumerate(csv_abierto):
			if c > 0:								# Si es filas de datos...
				if len(fila) != cant_campos:		# Si el largo de fila coincide con cant. campos...
					self.mensajes_error.append([c+1, "Se encontró distinta cantidad de campos.","Campos",])

		return 0


	def codigos(self, csv_abierto, codigo):
		""" Método que chequea que no haya codigos vacios en un archivo CSV ya abierto."""

		for c, fila in enumerate(csv_abierto):
			if c > 0:											# Si es filas de datos...
				if fila[codigo] == "" or fila[codigo] == " ":  	# Si el código está vacío...
					self.mensajes_error.append([c+1, "Se encontró un código vacío.","Códigos"])

		return 0


	def cantidades(self, csv_abierto, cantidad):
		""" Método que chequea que haya cantidades enteras en el campo "cantidad" de un
		archivo CSV	abierto."""

		for c, fila in enumerate(csv_abierto):
			if c > 0:								# Si es filas de datos...
				parte_entera = 0
				parte_fraccion = 0
				error = False

				try:
					valor = fila[cantidad]				# Obtenemos el string.
					p = valor.index(".")				# Obtenemos el punto decimal.
					parte_entera = int(valor[:p])		# Sacamos parte entera.
					parte_fraccion = int(valor[p + 1:]) # Y sacamos parte fracionaria.

				except ValueError:				# En caso de no poder castear...
					error = True

				except IndexError:				# En caso de encontrar un "fuera de índice"...
					error = True

				if error or parte_fraccion > 0:
					self.mensajes_error.append([c+1, "No contiene un valor entero.","Cantidades"])

		return 0


	def precios(self, csv_abierto, precio):
		""" Método que chequea que los campos "precio" de un archivo CSV contenga
			valores decimales. """

		for c, fila in enumerate(csv_abierto):
			if c > 0:							# Si es filas de datos...
				parte_entera = 0
				parte_fraccion = 0
				error = False

				try:
					valor = fila[precio]				# Obtenemos el string.
					parte_entera = int(valor[:-3])		# Sacamos parte entera.
					parte_fraccion = int(valor[-2:])	# Y sacamos parte fracionaria.

				except ValueError:				# En caso de no poder castear...
					error = True

				except IndexError:				# En caso de encontrar un "fuera de índice"...
					error = True

				if error:
					self.mensajes_error.append([c+1, "No contiene un valor decimal.","Precios"])

		return 0


# FIN