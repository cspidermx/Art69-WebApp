from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from webapp.models import User


class SearchArts(FlaskForm):
    srchstr = StringField('A Buscar: ', validators=[DataRequired()])
    submit = SubmitField('_______')


class LoginForm(FlaskForm):
    username = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Ingresar')


class RegistrationForm(FlaskForm):
    username = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repetir Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(fullname=username.data).first()
        if user is not None:
            raise ValidationError('Nombre de usuario no disponible.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Dirección de correo en uso por otro usuario.')


class EditProfileForm(FlaskForm):
    username = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    oldpassword = PasswordField('Password Anterior')
    newpassword = PasswordField('Password Nuevo')
    newpassword2 = PasswordField('Repetir Password Nuevo', validators=[EqualTo('newpassword')])
    submit = SubmitField('Enviar')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(fullname=username.data).first()
            if user is not None:
                raise ValidationError('Este nombre ya ha sido registrado.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Dirección de correo en uso por otro usuario.')

    def validate_oldpassword(self, pwd):
        if self.newpassword.data != "":
            user = User.query.filter_by(username=self.username.id).first()
            if user is None:
                raise ValidationError('Usuario desconocido. ')
            else:
                if not user.check_password(pwd.data):
                    raise ValidationError('Password anterior incorrecto.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Restablecer Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Dirección de correo no encontrada.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetir Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Solicitar Restablecer Password')


