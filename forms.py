from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import DateField

class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)], render_kw={"placeholder": "Nombre"})
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=64)], render_kw={"placeholder": "Apellido"})
    id=StringField('Identificacion', validators=[DataRequired(), Length(max=11)], render_kw={"placeholder": "Identificación"})
    fecha_na=DateField('Fecha de Nacimiento', validators=[DataRequired()], render_kw={"placeholder": "MM/DD/YYYY"}, format='%Y-%m-%d')
    sexo=SelectField('Sexo', validators=[DataRequired()], choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino'), ('No reporta', 'Prefiero no compartir')], default=2)
    phone=StringField('Telefono', validators=[DataRequired(), Length(max=10)], render_kw={"placeholder": "Teléfono"})
    pwd = PasswordField('Contraseña', validators=[DataRequired()], render_kw={"placeholder": "Contraseña"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Correo Electrónico"})
    ciudad=SelectField('Ciudad', validators=[DataRequired()], choices=[('Bogotá D.C', 'Bogotá D.C'), ('Cartagena', 'Cartagena'), ('Barranquilla', 'Barranquilla'), ( 'Cali', 'Cali'), ('Bucaramanga', 'Bucaramanga')])
    terms=BooleanField('Acepto terminos y condiciones', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Correo Electrónico"})
    pwd = PasswordField('Contraseña', validators=[DataRequired()], render_kw={"placeholder": "Contraseña"})
    remember_me = BooleanField('Recuérdame')
    submit2 = SubmitField('Iniciar Sesión', render_kw={"label": "Iniciar Sesión"})
    
    