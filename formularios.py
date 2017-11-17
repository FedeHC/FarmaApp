# -----------------------------------------------------------------------------
# Final de Paradigmas de Programación y Estructura de Datos
# (1° Año, 2° Cuatr. - 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Length


class Login(FlaskForm):
	"""	Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario
	de login al ingresar al sitio."""

	usuario = StringField(validators=[InputRequired(), Length(min=3)])
	clave = PasswordField(validators=[InputRequired(), Length(min=3)])
	submit = SubmitField()


class Registro(Login):
	"""	Clase que hereda de Login y que contiene los inputs necesarios para el formulario
	de registro del sitio."""

	repetir_clave = PasswordField(validators=[InputRequired(), Length(min=3)])


class Cambio_Clave(FlaskForm):
	"""	Clase que hereda de FlaskForm y que contiene los inputs necesarios para el formulario
	de cambio de clave (cuando se está logueado como usuario)."""

	vieja_clave = PasswordField(validators=[InputRequired(), Length(min=3)])
	nueva_clave = PasswordField(validators=[InputRequired(), Length(min=3)])
	confirmar_nueva_clave = PasswordField(validators=[InputRequired(), Length(min=3)])
	submit = SubmitField()
	

class Busqueda(FlaskForm):
	""" Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario
	de búsqueda (usado en 2 de las 4 consultas que el sitio brinda)."""

	buscar = StringField(validators=[InputRequired(), Length(min=3)])
	submit = SubmitField()


class Traer(FlaskForm):
	""" Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario
	de cantidad a traer (usado en 2 de las 4 consultas que el sitio brinda). """

	buscar = IntegerField(validators=[InputRequired()])
	submit = SubmitField()


class Exportar(FlaskForm):
	""" Clase que hereda de WTForms y que contiene un submit necesario para exportar resultados
	a un archivo CSV. """

	guardar = SubmitField()


# FIN