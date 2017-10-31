# FarmaApp

Aplicación web realizada como trabajo de parcial para las materias de [Paradigmas de Programación](http://leo.bitson.com.ar/ifts/par/) y [Estructura de datos](http://leo.bitson.com.ar/ifts/edd/), ambas materias de 1° año de la *[Tec. Sup. de Analista de Sistemas](http://www.ifts18.edu.ar/plan-de-estudios)* del [IFTS N°18](http://www.ifts18.edu.ar/).

* *Alumno: **Federico H. Cacace**.*
* *Profesor: **Leandro E. Colombo Viña**.*

![Imagen](https://i.imgur.com/nUSoQcD.png)

## Informe

### Flujo del programa/funcionamiento:

La aplicación parte desde [app.py](https://github.com/FedeHC/FarmaApp/blob/master/app.py), que redirige al HTML correspondiente de acuerdo a si hay un usuario logueado o no:

+ Si no hay usuario logueado, se redirige a [inicio.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/inicio.html) para que el mismo pueda loguearse.

+ Si se ha logueado con éxito, se redirige a [usuario.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/usuario.html), en donde se mostrarán las últimas 5 ventas realizadas (o lo que contenga [archivo.csv](https://github.com/FedeHC/FarmaApp/blob/master/archivo.csv) al momento de ejecturse la aplicación).
Desde allí puede elegirse las 4 consultas disponibles:
	+ **Productos por cliente** ([pxc.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pxc.html)): el usuario puede consultar todos los productos que compró un cliente determinado.
	+ **Clientes por producto** ([cxp.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cxp.html)): el usuario puede también consultar todos los clientes que compraron un producto especificado.
	+ **Productos más vendidos** ([pmv.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pmv.html)): el usuario puede traer acá una lista dos los productos que más se vendieron por unidad.
	+ **Clientes que más gastaron** ([cmg.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cmg.html)): el usuario puede traer acá una lista dos los clientes que más gastaron por venta.

	+ (El usuario puede elegir desloguearse al elegir el menu que lleva su nombre de usuario y hacer click en *salir*).

### Estructura de la aplicación:

#### [En raiz]

*  **[app.py](https://github.com/FedeHC/FarmaApp/blob/master/app.py):** el programa principal. El mismo importa e instancia:
	+ *Flask* y todas las extensiones empleadas (Flask-Bootstrap, Flask-Script)
	+ Las clases propias utilizadas para realizar las consultas.
	
    También contiene configuraciones varias para la app y los distintas rutas con el origen de los archivos de datos (a modo de constantes).
    
    Y por sobre todo contiene también todas las funciones necesarias para redirigir a los templates correspondientes según elija el usuario y las condiciones impuestas de acuerdo al caso.
    

* **[validar.py](https://github.com/FedeHC/FarmaApp/blob/master/validar.py):** el script que valida el [archivo.csv](https://github.com/FedeHC/FarmaApp/blob/master/archivo.csv) pasado como fuente de datos.


* **[consultas.py](https://github.com/FedeHC/FarmaApp/blob/master/consultas.py):**  el  que crea al anterior a modo de objeto y que contiene los métodos necesarios para realizar todas las consultas solicitadas.
	
    
* **[db.py](https://github.com/FedeHC/FarmaApp/blob/master/db.py):**  el script que permite guardar en [usuario_clave.csv](https://github.com/FedeHC/FarmaApp/blob/master/usuario_clave.csv) todos los usuarios ya registrados con sus respectivas constraseñas.


* **[archivo.csv](https://github.com/FedeHC/FarmaApp/blob/master/archivo.csv):** El fichero de texto plano que contiene toda la información de las ventas realizadas divididos en campos separados por coma. La primera fila indica el tipo y el orden de los campos.


* **[usuario_clave.csv](https://github.com/FedeHC/FarmaApp/blob/master/usuario_clave.csv):** Otro fichero de texto plano que guarda los usuarios y sus contraseñas correspondientes.

#### [En carpeta templates]

* **[base.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/base.html):** Contiene el navbar más la division contenedora principal del sitio. Se usa de base para los restantes templates y el navbar muestra las distintas consultas disponibles si el usuario está logueado (además de la opción de salir).
    

* **[inicio.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/inicio.html):** Contiene el formulario de logueo para ingresar al sitio.


* **[usuario.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/usuario.html):** Recibe al usuario recién logueado con las últimas ventas realizadas a modo de información útil.


* **[pxc.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pxc.html):** El template con el formulario para obtener los productos por cliente.

* **[cxp.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cxp.html):** El template con el formulario para obtener los clientes por producto.

* **[pmv.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pmv.html):** El template con el formulario para obtener los productos más vendidos.

* **[cmg.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cmg.html):** El template con el formulario para obtener a los clientes que más gastaron.


* **[404.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/404.html):** El template con mensaje de error en caso de no encontrarse la página buscada.

* **[500.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/500.html):** El template con mensaje de error en caso de surgir un error en el servidor.

#### [En carpeta static]

* **[estilos.css](https://github.com/FedeHC/FarmaApp/blob/master/static/estilos.css):** El archivo CSS con los estilos propios usados a lo largo del sitio.


* Carpeta **[imágenes](https://github.com/FedeHC/FarmaApp/tree/master/static/imagenes):** La carpeta que contiene el icono del sitio más las imágenes por para [404.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/404.html) y [500.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/500.html).


* Carpeta **[bootstrap](https://github.com/FedeHC/FarmaApp/tree/master/static/bootstrap):** Carpeta donde se descarga todo el contenido necesario para usar [Bootstrap](http://getbootstrap.com/docs/3.3/getting-started/#download) y [jQuery](http://jquery.com/download/) en nuestra aplicación en modo local (evitando usar el CDN por defecto).


### Clases usadas en la aplicación:

*  Clase **DB** (en [db.py](https://github.com/FedeHC/FarmaApp/blob/master/db.py#L8)): Clase que recibe un nombre de archivo en su constructor y que cuenta con los métodos necesarios para leer y chequear los usuarios/contraseña registrados.


*  Clase **Csv** (en [validar.py](https://github.com/FedeHC/FarmaApp/blob/master/validar.py#L9)): Clase que recibe en su constructor un nombre de archivo como fuente de *datos* y un archivo *log* para guardar errores. Cuenta con los métodos para abrir el archivo fuente y validar sus campos fila por fila.


*  Clase **MiExcepcion** (en [validar.py](https://github.com/FedeHC/FarmaApp/blob/master/validar.py#L222)): Clase usada a modo de excepción personalizada en la clase **Csv** cuando surgen en esta mensajes de error a lo largo de las validaciones.


*  Clase **Consultas** (en [consultas.py](https://github.com/FedeHC/FarmaApp/blob/master/consultas.py#L8)): Clase que también recibe en su constructor un nombre de archivo como fuente de *datos* y un archivo *log* para guardar errores. Esta instancia un objeto de la clase **Csv**, y si su validación es correcta entonces brinda los métodos necesarios para realizar todas las consultas de datos que se pueden hacer a lo largo del sitio web.


*  Clase **Valores** (en [consultas.py](https://github.com/FedeHC/FarmaApp/blob/master/consultas.py#L174)): Clase que recibe solamente un nombre de campo y que representa en forma de lista de listas los resultados utilizados en uno de los métodos de la clase **Consultas**. En concreto, contiene los métodos necesarios para encontrar, sumar, agregar, ordenar/recortar/devolver los resultados en dicha lista.


*  Clase **Login** (en [formularios.py](https://github.com/FedeHC/FarmaApp/blob/master/formularios.py#L13)): Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario de logueo en [inicio.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/inicio.html).


*  Clase **Busqueda** (en [formularios.py](https://github.com/FedeHC/FarmaApp/blob/master/formularios.py#L22)): Clase que también hereda de WTForms y que contiene los inputs necesarios para los formulario de búsqueda en [pxc.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pxc.html) y [cxp.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cxp.html)


*  Clase **Traer** (en [formularios.py](https://github.com/FedeHC/FarmaApp/blob/master/formularios.py#L30)): Clase que también ereda de WTForms y que contiene los inputs necesarios para los formulario de búsqueda en [pmv.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pmv.html) y [cmg.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cmg.html)


## Instalación/Requisitos
En caso de instalar la app desde el código fuente, es necesario tener instalados [Python 3](https://www.python.org/downloads/) y [Flask](http://flask.pocoo.org/)  nuestro sistema operativo.

Además, es necesario también las siguientes extensiones:
  * [Flask_WTF](https://flask-wtf.readthedocs.io/)
  * [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
  * [Flask-Script](https://flask-script.readthedocs.io/)


(Para más detalles chequear [requirements.txt](https://github.com/FedeHC/FarmaApp/blob/master/requirements.txt))

 Se recomienda emplear un entorno virtual como [VirtualEnv](https://virtualenv.pypa.io/) o [VirtualEnvWrapper](https://virtualenvwrapper.readthedocs.io/) para ejecutar la app con dichas extensiones.]