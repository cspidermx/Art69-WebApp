from webapp import wappdb
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from webapp import login
from time import time
import jwt
from webapp import app
from sqlalchemy.sql.expression import func
from Crypto.Cipher import AES


def encript_id(id_txt):
    n = 16 - len(str(id_txt))
    string_val = "".join(" " for i in range(n)) + str(id_txt)
    encryption_suite = AES.new(app.config['SECRET_KEY'].encode("ISO-8859-1"), AES.MODE_CBC,
                               iv=app.config['SECRET_IV'].encode("ISO-8859-1"))
    cipher_text = encryption_suite.encrypt(string_val.encode("ISO-8859-1"))
    return cipher_text.decode("ISO-8859-1")


class DataArt69b(wappdb.Model):
    __tablename__ = 'sat_art69b'

    id = wappdb.Column(wappdb.Integer, primary_key=True)
    id_info = wappdb.Column(wappdb.Integer, primary_key=True)
    rfc = wappdb.Column(wappdb.String, nullable=False)
    nombre = wappdb.Column(wappdb.String, nullable=False)
    situacion = wappdb.Column(wappdb.String, nullable=False)
    numofi_presuncion = wappdb.Column(wappdb.String, nullable=False)
    fechaofi_presuncion = wappdb.Column(wappdb.Date, nullable=False)
    numofi_desvirtuado = wappdb.Column(wappdb.String)
    fechaofi_desvirtuado = wappdb.Column(wappdb.Date)
    numofi_definitivo = wappdb.Column(wappdb.String)
    fechaofi_definitivo = wappdb.Column(wappdb.Date)
    numofi_sentfav = wappdb.Column(wappdb.String)
    fechaofi_sentfav = wappdb.Column(wappdb.Date)


class User(UserMixin, wappdb.Model):
    id = wappdb.Column(wappdb.Integer, primary_key=True)
    email = wappdb.Column(wappdb.String, index=True, unique=True)
    fullname = wappdb.Column(wappdb.String, index=True, unique=True)
    password_hash = wappdb.Column(wappdb.String)
    level = wappdb.Column(wappdb.Integer)
    activo = wappdb.Column(wappdb.Boolean)

    def enc_id(self):
        return encript_id(self.id)

    def new_id(self):
        mx = wappdb.session.query(func.max(User.id)).one()
        if mx[0] is not None:
            self.id = mx[0] + 1
        else:
            self.id = 1
        self.level = 1
        self.activo = True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Usuario {}>'.format(self.email)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'restablecer_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            idtkn = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['restablecer_password']
        except jwt.ExpiredSignatureError:
            return 'Firma ha expirado. Intente firmarse de nuevo.'
        except jwt.InvalidTokenError:
            return 'Token invalido. Intente firmarse de nuevo.'
        return User.query.get(idtkn)


@login.user_loader
def load_user(idusr):
    return User.query.get(int(idusr))
