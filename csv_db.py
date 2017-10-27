# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

import csv


class DB():
	""" Clase para manipular un CSV pasado como argumento. """
	
	# CONSTRUCTOR:
	def __init__(self, RUTA_ARCHIVO):
		# Local:
		self.RUTA_ARCHIVO = RUTA_ARCHIVO


	def leer(self):
		""" Método que lee un CSV a partir de una ruta determinada. """
		
		try:
			archivo = open(self.RUTA_ARCHIVO ,'r')
			csv_abierto = csv.reader(archivo, delimiter='|')
			return archivo, csv_abierto

		except IOError as e:
			print("ERROR al leer usuario/clave:", e)
			return None, None		


	def chequear(self, campo1, campo2):
		""" Método que lee un CSV y retorna 'True' si se encontró un campo determinado.
		Devuelve 'False' en caso contrario."""
		
		archivo, csv = self.leer()
		
		rto_campo1 = False
		rto_campo2 = False

		if(archivo):
			for c, fila in enumerate(csv):
				if c > 0:
					if fila[0] == campo1:
						rto_campo1 = True
						if fila[1] == campo2:
							rto_campo2 = True

			archivo.close()

		return rto_campo1, rto_campo2


	def crear(self, campo1, campo2):
		""" Método que lee un CSV, recibe un usuario y clave y lo agrega al archivo CSV."""
		
		try:
			archivo = open(self.RUTA_ARCHIVO ,'a')
			archivo.writelines(['\n' + campo1 + '|' + campo2])
			archivo.close()

		except IOError as e:
			print("ERROR al escribir en BD:", e)

		finally:
			return 0


	def traer_usuarios(self):
		""" Método que retorna una lista de todos los usuarios guardados en CSV. """

		archivo, csv = self.leer()

		lista_users = []		# Creando lista donde se guardarán todos los usuarios.
		for c, fila in enumerate(csv):
			if c > 0:
				lista_users.append(fila[0])

		return lista_users

# FIN