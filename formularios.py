# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
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

	usuario = StringField("Usuario", validators=[InputRequired(), Length(min=3)])
	clave = PasswordField("Clave", validators=[InputRequired(), Length(min=3)])
	submit = SubmitField("Enviar")


class Busqueda(FlaskForm):
	""" Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario
	de búsqueda (usado en 2 de las 4 consultas que el sitio brinda)."""

	buscar = StringField("Buscar", validators=[InputRequired(), Length(min=3)])
	submit = SubmitField("Enviar")


class Traer(FlaskForm):
	""" Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario
	de cantidad a traer (usado en 2 de las 4 consultas que el sitio brinda). """

	buscar = IntegerField("Buscar", validators=[InputRequired()])
	submit = SubmitField("Enviar")


# FIN