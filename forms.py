from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, EqualTo

class JogoForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    genero = StringField('Género', validators=[DataRequired()])
    plataforma = StringField('Plataforma', validators=[DataRequired()])
    submeter = SubmitField('Gravar')

class LoginForm(FlaskForm):
    username = StringField('Utilizador', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submeter = SubmitField('Entrar')

class RegistoForm(FlaskForm):
    username = StringField('Utilizador', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmar = PasswordField('Confirmar Password', validators=[EqualTo('password')])
    submeter = SubmitField('Registar')