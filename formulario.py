from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class Login(FlaskForm):
	""" Clase que hereda de WTForms y que contiene los inputs necesarios para el formulario
	de logueo. """
	usuario = StringField("Usuario", validators=[DataRequired()])
	clave = PasswordField("Clave", validators=[DataRequired()])
	submit = SubmitField("Enviar")


# FIN