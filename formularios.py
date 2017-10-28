# -----------------------------------------------------------------------------
# Parcial de Estructura de Datos (2° Cuatr. 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class Login(FlaskForm):
	"""	Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario
	de login al ingresar al sitio.
	"""

	usuario = StringField("Usuario", validators=[DataRequired()])
	clave = PasswordField("Clave", validators=[DataRequired()])
	submit = SubmitField("Enviar")


class Busqueda(FlaskForm):
	""" Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario
	de búsqueda (usado en las 4 consultas que el sitio debe brindar).
	"""

	buscar = StringField("Buscar", validators=[DataRequired()])
	submit = SubmitField("Buscar")


# FIN