# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

class DB():
	""" Clase para manipular un CSV pasado como argumento. """

	def __init__(self, nombre_archivo):
		""" Constructor de la clase DB. """
		self.nombre_archivo = nombre_archivo


	def leer(self):
		""" Método que lee un CSV a partir de una ruta determinada. 
			- Devuelve objeto open() y objeto csv.reader() si no hay problemas. 
			- Caso contrario, se retorna 2 'None'. """
		
		try:
			import csv

			archivo = open(self.nombre_archivo ,'r')
			csv_abierto = csv.reader(archivo, delimiter='|')
			return archivo, csv_abierto

		except IOError as e:
			print("ERROR al leer usuario/clave:", e)
			return None, None		


	def chequear(self, campo1, campo2):
		""" Método que lee un CSV y busca un campo determinado.
			- Devuelve 'True' en caso de encontrarse.
			- Devuelve 'False' en caso contrario."""
		
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


# FIN