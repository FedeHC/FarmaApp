# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

class DB():
	""" Clase para leer y chequear campos a partir de un CSV determinado. """

	def __init__(self, nombre_archivo):
		"""	Constructor de la clase DB.

		Args:
			nombre_archivo: El nombre de archivo en el que se guardará user y pass.
		"""
		
		self.nombre_archivo = nombre_archivo


	def leer(self):
		"""	Método que lee un CSV a partir de un archivo CSV determinado.

		Returns:
			- archivo: Un objeto open() obtenido a partir de nombre_archivo.
			- None: en caso de surgir IOError.
			
			- csv_abierto: Un objeto csv.reader() obtenido a partir del objeto open().
			- None: en caso de surgir IOError. 
		
		Raises:
			IOError: ERROR al leer usuario/clave: (...).
		"""
		
		try:
			import csv
			archivo = open(self.nombre_archivo ,'r')
			csv_abierto = csv.reader(archivo, delimiter='|')
			return archivo, csv_abierto

		except IOError as e:
			print("ERROR al leer usuario/clave:", e)
			return None, None		


	def chequear(self, campo1, campo2):
		"""
		Método que lee un archivo CSV determinado y busca en 2 campos pasados como argumentos.

		Returns:
			- rto_campo1: Un 'True' en caso de coincidencia, 'False' en caso contrario.
			- rto_campo2: Un 'True' en caso de coincidencia, 'False' en caso contrario.
		"""

		archivo, csv = self.leer()
		
		rto_campo1 = False
		rto_campo2 = False

		if archivo:
			for c, fila in enumerate(csv):
				if c > 0:
					if fila[0] == campo1:
						rto_campo1 = True
						if fila[1] == campo2:
							rto_campo2 = True
			archivo.close()

		return rto_campo1, rto_campo2


# FIN