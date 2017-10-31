# FarmaApp

Aplicación web realizada como trabajo de parcial para las materias de [Paradigmas de Programación](http://leo.bitson.com.ar/ifts/par/) y [Estructura de datos](http://leo.bitson.com.ar/ifts/edd/), ambas materias de 1° año de la *[Tec. Sup. de Analista de Sistemas](http://www.ifts18.edu.ar/plan-de-estudios)* del [IFTS N°18](http://www.ifts18.edu.ar/).

* *Alumno: **Federico H. Cacace**.*
* *Profesor: **Leandro E. Colombo Viña**.*


![Imagen](https://i.imgur.com/nUSoQcD.png)

## Informe

### Modo de uso:

La app cuenta con un login donde el usuario debe loguearse para poder ingresar y realizar las consultas disponibles. 

* **Nota:** ver archivo [usuario_clave.csv](https://github.com/FedeHC/FarmaApp/blob/master/usuario_clave.csv) para ver los pares usuario/contraseña ya registrados.

Una vez logueado, se visualiza un título de bienvenida seguido de las últimas ventas realizadas. Desde allí el usuario puede optar por realizar cualquiera de las 4 consultas disponibles o salir.


### Flujo del programa:

La aplicación parte desde [app.py](https://github.com/FedeHC/FarmaApp/blob/master/app.py), que redirige al HTML correspondiente de acuerdo a si hay un usuario logueado o no:

+ Si no hay usuario logueado, se redirige a [inicio.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/inicio.html) para que el mismo pueda loguearse.

+ Si se ha logueado con éxito, se redirige a [usuario.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/usuario.html), en donde se mostrarán las últimas 5 ventas realizadas; o lo que contenga el [archivo.csv](https://github.com/FedeHC/FarmaApp/blob/master/archivo.csv) al momento de ejecutarse la app, o mensajes de error si no se encuentra éste bien validado.
En caso de estar bien validado, desde ahí puede elegirse las 4 consultas que se disponen:
	+ **Productos por cliente** ([pxc.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pxc.html)): el usuario puede consultar todos los productos que compró un cliente determinado.
	+ **Clientes por producto** ([cxp.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cxp.html)): el usuario puede también consultar todos los clientes que compraron un producto en particular.
	+ **Productos más vendidos** ([pmv.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pmv.html)): el usuario puede solicitar una lista con los productos que más se vendieron por unidad, ingresando la cantidad a mostrar.
	+ **Clientes que más gastaron** ([cmg.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cmg.html)): el usuario puede solicitar una lista con los clientes que más gastaron por venta, ingresando la cantidad a mostrar.

	+ (El usuario puede elegir desloguearse al elegir el menu que lleva su nombre-->*salir*).

### Estructura de la aplicación:

#### [En raiz]

*  **[app.py](https://github.com/FedeHC/FarmaApp/blob/master/app.py):** el programa principal. El mismo importa e instancia los siguientes:
	+ *Flask* y todas las extensiones empleadas (Flask-Bootstrap, Flask-Script)
	+ Las clases propias utilizadas para realizar las consultas.
	
    También contiene configuraciones varias y las distintas rutas con el origen de los archivos de datos.
    
    Su función pricipal es contener todas las funciones necesarias para redirigir a los templates correspondientes según elija el usuario y las condiciones impuestas de acuerdo al caso (si está logueado, si hay datos disponibles, si la validación fue correcta, etc.)
    

* **[validar.py](https://github.com/FedeHC/FarmaApp/blob/master/validar.py):** el script que valida el [archivo.csv](https://github.com/FedeHC/FarmaApp/blob/master/archivo.csv) pasado como fuente de datos de las todas las ventas realizadas.


* **[consultas.py](https://github.com/FedeHC/FarmaApp/blob/master/consultas.py):**  el  que crea al anterior a modo de objeto y que contiene los métodos necesarios para realizar todas las consultas solicitadas a lo largo del sitio.
	
    
* **[db.py](https://github.com/FedeHC/FarmaApp/blob/master/db.py):**  el script que permite guardar en [usuario_clave.csv](https://github.com/FedeHC/FarmaApp/blob/master/usuario_clave.csv) todos los pares usuario/contraseña.


* **[archivo.csv](https://github.com/FedeHC/FarmaApp/blob/master/archivo.csv):** El fichero de texto plano que contiene toda la información de las ventas realizadas divididos en campos separados por coma. La primera fila indica el tipo y el orden de los campos (éste puede venir en cualquier orden, siempre que sean solamente los 5 campos especificados en el ejercicio).


* **[usuario_clave.csv](https://github.com/FedeHC/FarmaApp/blob/master/usuario_clave.csv):** Otro fichero de texto plano que guarda los pares usuario/contraseña correspondientes.

#### [En carpeta templates]

* **[base.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/base.html):** Contiene el navbar más la division contenedora principal del sitio. Se usa justamente de base para los demás templates. El navbar varia su contenido, monstrando las distintas consultas disponibles y el nombre del usuario si éste está logueado (incluyendo la opción de salir).
    

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


* Carpeta **[imágenes](https://github.com/FedeHC/FarmaApp/tree/master/static/imagenes):** La carpeta que contiene el icono del sitio más las imágenes usadas para [404.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/404.html) y [500.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/500.html).


* Carpeta **[bootstrap](https://github.com/FedeHC/FarmaApp/tree/master/static/bootstrap):** Carpeta donde se descarga todo el contenido necesario para usar [Bootstrap](http://getbootstrap.com/docs/3.3/getting-started/#download) y [jQuery](http://jquery.com/download/) en nuestra aplicación a modo local (evitando usar el CDN).


### Clases usadas en la aplicación:

*  Clase **DB** (en [db.py](https://github.com/FedeHC/FarmaApp/blob/master/db.py#L8)): Clase que recibe un nombre de archivo en su constructor y que cuenta con los métodos necesarios para leer y chequear todos los pares usuario/contraseña ya registrados.


*  Clase **Csv** (en [validar.py](https://github.com/FedeHC/FarmaApp/blob/master/validar.py#L9)): Clase que recibe en su constructor un nombre de archivo como fuente de *datos* y un archivo *log* para guardar errores. Cuenta con los métodos para abrir el archivo fuente y validar sus campos, fila por fila.


*  Clase **MiExcepcion** (en [validar.py](https://github.com/FedeHC/FarmaApp/blob/master/validar.py#L222)): Clase usada a modo de excepción personalizada en la clase **Csv** cuando surgen en esta mensajes de error a lo largo de las validaciones.


*  Clase **Consultas** (en [consultas.py](https://github.com/FedeHC/FarmaApp/blob/master/consultas.py#L8)): Clase que también recibe en su constructor un nombre de archivo como fuente de *datos* y un archivo *log* para guardar errores. Esta misma clase instancia un objeto de la clase **Csv**, y si la validación del CSV en esta última es correcta entonces la clase *Consultas* brinda los métodos necesarios para realizar todas las consultas de datos que se pueden hacer a lo largo del sitio.


*  Clase **Valores** (en [consultas.py](https://github.com/FedeHC/FarmaApp/blob/master/consultas.py#L174)): Clase que recibe solamente un nombre de campo y que representa en forma de *lista de listas* los resultados utilizados en uno de los métodos de la clase **Consultas**. En concreto, contiene los métodos necesarios para encontrar, sumar, agregar, ordenar/recortar/devolver los resultados en dicha lista.


*  Clase **Login** (en [formularios.py](https://github.com/FedeHC/FarmaApp/blob/master/formularios.py#L13)): Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario de logueo en [inicio.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/inicio.html).


*  Clase **Busqueda** (en [formularios.py](https://github.com/FedeHC/FarmaApp/blob/master/formularios.py#L22)): Clase que también hereda de WTForms y que contiene los inputs necesarios para los formulario de búsqueda en [pxc.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pxc.html) y [cxp.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cxp.html)


*  Clase **Traer** (en [formularios.py](https://github.com/FedeHC/FarmaApp/blob/master/formularios.py#L30)): Clase que también hereda de WTForms y que contiene los inputs necesarios para los formulario de búsqueda en [pmv.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/pmv.html) y [cmg.html](https://github.com/FedeHC/FarmaApp/blob/master/templates/cmg.html)


## Instalación/Requisitos
En caso de instalar la app desde el código fuente, es necesario tener instalados [Python 3](https://www.python.org/downloads/) y [Flask](http://flask.pocoo.org/)  nuestro sistema operativo.

Además, es necesario también contar con las siguientes extensiones:
  * [Flask_WTF](https://flask-wtf.readthedocs.io/)
  * [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
  * [Flask-Script](https://flask-script.readthedocs.io/)


(Para más detalles chequear [requirements.txt](https://github.com/FedeHC/FarmaApp/blob/master/requirements.txt))

 Se recomienda emplear un entorno virtual como [VirtualEnv](https://virtualenv.pypa.io/) o [VirtualEnvWrapper](https://virtualenvwrapper.readthedocs.io/) para ejecutar la app con dichas extensiones.