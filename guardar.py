# -----------------------------------------------------------------------------
# Final de Paradigmas de Programación y Estructura de Datos
# (1° Año, 2° Cuatr. - 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

class Guardar():
	""" Clase que guarda resultados recibidos en CSV. """

	def __init__(self, archivo, log):
		""" Constructor de la clase Guardar. 

		Args:
			archivo: El archivo que contiene todo el CSV.
			log: El archivo que guardará todos los mensajes de error, en caso de haberlos.
		"""

		import validar

		self.archivo = archivo
		self.log = log

