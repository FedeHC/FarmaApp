# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

class Consultas():
	""" La clase que realiza las consultas solicitadas en las consignas. """

	def __init__(self, archivo, log):
		""" Constructor de la clase Consultas. 

		Args:
			archivo: El archivo que contiene todo el CSV.
			log: El archivo que guardará todos los mensajes de error, en caso de haberlos.
		"""
		import validar

		self.archivo = archivo
		self.log = log

		# Creando un objeto de la clase 'Csv':
		self.csv = validar.Csv(self.archivo, self.log)

		# Recordar que 'self.csv.ok' guarda el estado de la validación del CSV.


	def listar_x_en_y(self, campo1, campo2, palabra):
		""" Método que busca y devuelve filas de un CSV a partir de una palabra que	concuerde
		con el contenido de un campo.

		Args:
			campo1: Un nombre del campo que debe coincidir con alguno del diccionario 'campos'.
			campo2: Otro nombre del campo que debe coincidir con alguno del diccionario 'campos'.
			palabra: Una palabra recibida desde formulario html a buscar en campo2.

		Returns:
			resultados: Las filas en donde hubo coincidencias de 'palabra' con 'campo2'.
			columnas: Una lista con las posiciones de columna de las proceden campo1 y campo2.
		"""

		# Obtenemos las ubicaciones de los campos ya sacados en 'validar.py':
		nro_campo1 = self.csv.campos[campo1]
		nro_campo2 = self.csv.campos[campo2]
		columnas = [nro_campo1, nro_campo2]

		# Abrimos el archivo y el objeto CSV:
		archivo, csv = self.csv.abrir_csv(self.archivo)

		resultados = []	# Lista para guardar los resultados.
		
		for c, fila in enumerate(csv):			# Recorremos el CSV.
			if c == 0:							# Si es la 1ra fila...
				resultados.append(fila)
			else:										# Si son filas de datos...
				if palabra in fila[nro_campo2].lower():	# Si la palabra está en el campo2...
					resultados.append(fila)

		archivo.seek(0)							# Ponemos el cursor del archivo en cero.
		return resultados, columnas				# Retornamos listas de resultados y columnas.


	def listar_los_mas_x(self, campo1, campo2, cantidad):
		""" Método que busca y muestra en pantalla los N elementos del 'campo1' que más suman
		del	"campo2". 

		Args:
			campo1: Un nombre del campo que debe coincidir con alguno del diccionario 'campos'.
			campo2: Otro nombre del campo que debe coincidir con alguno del diccionario 'campos'.
			cantidad: Un int para delimitar la cantidad de resultados obtenidos.

		Returns:
			resultados: Las filas en donde hubo coincidencias de 'palabra' con 'campo2'.
			columnas: Una lista con las posiciones de columna de las proceden campo1 y campo2.
		"""

		# Obtenemos las ubicaciones de los campos ya sacados en 'validar.py':
		nro_campo1 = self.csv.campos[campo1]
		nro_campo2 = self.csv.campos[campo2]
		columnas = [nro_campo1, nro_campo2]

		# Abrimos el archivo y el objeto CSV:
		archivo, csv = self.csv.abrir_csv(self.archivo)

		resultados = Elem_y_cant()					# Para guardar los resultados.

		# Recorremos el CSV:
		for c, fila in enumerate(csv):
			if c > 0:								# Si son las filas de datos...
				
				# Asignamos 2 variables para guardar el elemento y el valor:
				elemento = fila[nro_campo1]
				valor = fila[nro_campo2]

				try:
					# Según la naturaleza deñ campo2, casteamos de un modo u otro:
					if campo2 == 'cantidad':
						valor = int(float(valor))	# Paso a 'float' 1ro y a 'int' después...
					if campo2 == 'precio':
						valor = float(valor)

				except ValueError:
					print(" - No se ha podido castear valor, continuando...")

				# Agregamos o sumamos al diccionario:
				if elemento in resultados.dicc:
					resultados.sumar(elemento, valor)
				else:
					resultados.agregar(elemento, valor)

		# Obtenemos en forma de lista lo almacenado en el objeto 'resultados', limitado
		# a la cantidad pasada por el usuario:
		lista = resultados.ordenar_y_devolver(cantidad)

		# Mostramos los resultados de la lista obtenida en pantalla:
		for e, v in lista:
			if campo2 == 'cantidad':
				v = str(v) + ' un.'
			if campo2 == 'precio':
				v = '$' + str(v)
			self.mostrar_valores_en_2_columnas(e, v)

		return 0


	def ultimos_resultados(self, cantidad=5):
		""" Método que devuelve los últimos 5 resultados de un CSV .
		Args:
			cantidad: Un nombre del campo que debe coincidir con alguno del diccionario
				'campos' de la clase. Valor por defecto: 5.

		Returns:
			resultados: Una lista con la 1ra fila + los últimos resultados del CSV.
			nro_filas: Un Int con el número de fila del CSV desde donde se empiezan a obtener
				los resultados.
			cantidad: El int que se pasó como argumento y que determina la cantidad de
				resultados a traer.
		"""

		# Abrimos el archivo y el objeto CSV:
		archivo, csv = self.csv.abrir_csv(self.archivo)

		resultados = []							# Lista para guardar los resultados.

		# Recorremos el CSV para agregar solo las últimas filas:
		contador = 0
		for fila in reversed(list(csv)):
			if contador < cantidad:
				resultados.append(fila)
				contador = contador + 1

		archivo.seek(0)							# Ponemos el cursor del archivo en cero.

		# Recorremos nuevamente el CSV para agregar solo la primera fila y también
		# obtener el total de filas:
		nro_filas = 0
		for c, fila in enumerate(csv):			
			if c == 0:							# Si es la 1ra fila...
				resultados.append(fila)
			else:
				nro_filas = c

		nro_filas = nro_filas - cantidad 		# Restamos cantidad al nro_filas.
		resultados = reversed(resultados)		# Damos vuelta la lista.

		archivo.seek(0)							# Ponemos el cursor del archivo en cero.
		return resultados, nro_filas, cantidad 	# Retornamos lista y demás valores.
			

class Elem_y_cant():
	""" Clase que representa internamente en forma de diccionario elementos y cantidades."""

	# Constructor:
	def __init__(self):
		""" Constructor de la clase Elem_y_cant. """
		self.dicc = {}


	def agregar(self, clave, valor):
		""" Método que agrega un par clave/valor al diccionario. 

		Args:
			clave: La clave que se agregará al diccionario.
			valor: Y el valor que se agregará al diccionario a esa clave.
		"""
		self.dicc.update({clave:valor})
		return 0


	def sumar(self, clave, valor):
		""" Método que suma un valor a otro dentro del diccionario.

		Args:
			clave: La clave que se sumará al diccionario.
			valor: Y el valor que se sumará al diccionario a esa clave.
		"""
		self.dicc[clave] = self.dicc[clave] + valor
		return 0


	def ordenar_y_devolver(self, cantidad):
		""" Método que obtiene los elementos de un diccionario y los guarda ordenados en
		una lista.
		
		Args:
			cantidad: Un int que especifica la cantidad de elementos al que se deberá delimitar
				una lista.

		Returns:
			lista: La nueva lista ordenada.
		"""

		# Acá uso comprensión de listas:
		lista = [[clave, self.dicc[clave]] for clave in sorted(self.dicc, key=self.dicc.get, reverse=True)]
		lista = lista[:cantidad]
		return lista


# FIN