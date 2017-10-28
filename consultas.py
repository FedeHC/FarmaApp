# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

class Consultas():
	""" La clase que realiza las consultas solicitadas en las consignas. """

	# Constructor:
	def __init__(self, archivo="archivo.csv", log="error.log"):
		""" Constructor de la clase Consultas. """

		self.archivo = archivo
		self.log = log
		self.todo_ok = None

		self.chequeando()		# Llamando a método que inicia el chequeo del CSV.


	def chequeando(self):
		""" Método que inicia la validación de un CSV a partir de un módulo importado. """
		
		# Importando módulo 'validar.py':
		import validar

		# Creando un objeto de la clase 'Csv':
		self.csv = validar.Csv(self.archivo, self.log)

		# Si el CSV está correctamente validado:
		if self.csv.ok:
			self.todo_ok = True
		else:
			self.todo_ok = False

		return 0


	def listar_x_en_y(self, campo1, campo2, palabra):
		""" Método que busca y devuelve filas de un CSV a partir de una palabra que	concuerde
		con el contenido de un campo (palabra y campo son pasados como parámetros).
			- Se devuelve una lista con los resultados (si los hay) y otra con los números de
			las posiciones de las columnas """

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


	def listar_los_mas_x(self, campo1, campo2, palabra):
		""" Método que busca y muestra en pantalla los N elementos del 'campo1' que más suman del
		"campo2". Ambos son pasados como parámetros. """

		# Obtenemos las ubicaciones de los campos ya sacados en 'validar.py':
		nro_campo1 = self.csv.campos[campo1]
		nro_campo2 = self.csv.campos[campo2]

		# Abrimos el archivo y el objeto CSV:
		archivo, csv = self.csv.abrir_csv(self.archivo)

		# Creamos un objeto de la clase 'Elem_y_cant' para representar todos los elementos
		# de un campo y las cantidades que estos acumulan a lo largo de otro campo en un
		# archivo CSV:
		resultados = Elem_y_cant()

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
		print(" - Listando los {}:\n".format(len(lista)))

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
			- Se devuelve una lista con el resultado. """

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
	""" Clase que representa internamente en forma de diccionario elementos y cantidades. 
	  Como claves se representa todos los elementos encontrados desde un campo determinado dentro
	  de un CSV. Y como valores, las cantidades que los 1ros acumulan a partir de un 2do campo
	  del CSV en cuestión. """

	# Constructor:
	def __init__(self):
		""" Constructor de la clase Elem_y_cant. """
		self.dicc = {}


	def agregar(self, clave, valor):
		""" Método que agrega un par clave/valor al diccionario. """
		self.dicc.update({clave:valor})
		return 0


	def sumar(self, clave, valor):
		""" Método que suma un valor a otro dentro del diccionario. """
		self.dicc[clave] = self.dicc[clave] + valor
		return 0


	def ordenar_y_devolver(self, cantidad):
		""" Método que obtiene los elementos de un diccionario y los guarda ordenados en
		una lista.
			- Se retorna una lista. """

		# Acá uso comprensión de listas:
		lista = [[clave, self.dicc[clave]] for clave in sorted(self.dicc, key=self.dicc.get, reverse=True)]
		lista = lista[:cantidad]
		return lista


# FIN