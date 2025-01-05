from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
class GroupsForm(FlaskForm):
    name = StringField(
        'Nombre de la Familia', 
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Length(max=150, message="El nombre no puede tener más de 150 caracteres.")
        ]
    )
    submit = SubmitField('Crear Familia')