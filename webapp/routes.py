from flask import render_template, flash, redirect, url_for
from webapp import app
from webapp.forms import LoginForm
from flask_login import current_user, login_user
from webapp.models import User, DataArt69b, DataArt69, Info69, Info69b
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from webapp import wappdb
from webapp.forms import RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, SearchArts
from email.message import EmailMessage
import threading
import smtplib
from Crypto.Cipher import AES
from sqlalchemy import or_, and_
from sqlalchemy.sql.expression import func
import locale


def decrypt_id(ctxt):
    decryption_suite = AES.new(app.config['SECRET_KEY'].encode("ISO-8859-1"), AES.MODE_CBC,
                               iv=app.config['SECRET_IV'].encode("ISO-8859-1"))
    ptext = decryption_suite.decrypt(ctxt).decode("utf-8").strip()
    return ptext


def send_async_email(app_, srv, msge):
    with app_.app_context():
        if not srv['SSL']:
            smtp = smtplib.SMTP(srv['server'], srv['port'])
            smtp.starttls()
        else:
            smtp = smtplib.SMTP_SSL(srv['server'], srv['port'])  # Use this for Nemaris Server
        smtp.login(srv['user'], srv['password'])
        smtp.sendmail(msge['From'], msge['To'], msge.as_string())
        smtp.quit()


def send_email(server, msg):
    threading.Thread(target=send_async_email, args=(app, server, msg)).start()


def send_password_reset_email(usr):
    smtpserver = app.config['SMTP']

    msg = EmailMessage()
    msg['Subject'] = "Restablecer Password - Revision Art. 69 y 69b"
    msg['From'] = smtpserver['user']
    msg['To'] = usr.email
    msg.set_type('text/html')

    token = usr.get_reset_password_token()
    msg.set_content(render_template('email/reset_password.txt', user=usr, token=token))
    html_msg = render_template('email/reset_password.html', user=usr, token=token)
    msg.add_alternative(html_msg, subtype="html")

    send_email(smtpserver, msg)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    frmss = SearchArts()
    mx = wappdb.session.query(func.max(Info69b.id)).one()
    if mx[0] is not None:
        if69b = Info69b.query.filter_by(id=mx[0]).first()
    else:
        if69b = None
    if69 = Info69.query.first()
    updates = (if69b, if69)
    a69b = None
    a69 = None
    if frmss.validate_on_submit():
        likesrch = '%' + str(frmss.srchstr.data).upper() + '%'
        a69b = {'DEFINITIVO': DataArt69b.query.filter(and_(DataArt69b.situacion.ilike('definitivo'),
                                                    or_(DataArt69b.rfc.like(likesrch),
                                                        DataArt69b.nombre.like(likesrch)))).order_by(
            DataArt69b.situacion.desc()).all(),
                'PRESUNTO': DataArt69b.query.filter(and_(DataArt69b.situacion.ilike('presunto'),
                                                or_(DataArt69b.rfc.like(likesrch),
                                                    DataArt69b.nombre.like(likesrch)))).order_by(
            DataArt69b.situacion.desc()).all(),
                'DESVIRTUADO': DataArt69b.query.filter(and_(DataArt69b.situacion.ilike('desvirtuado'),
                                                or_(DataArt69b.rfc.like(likesrch),
                                                    DataArt69b.nombre.like(likesrch)))).order_by(
            DataArt69b.situacion.desc()).all(),
                'SENTENCIA FAVORABLE': DataArt69b.query.filter(and_(DataArt69b.situacion.ilike('sentencia favorable'),
                                                or_(DataArt69b.rfc.like(likesrch),
                                                    DataArt69b.nombre.like(likesrch)))).order_by(
            DataArt69b.situacion.desc()).all()}
        a69 = DataArt69.query.filter(
            or_(DataArt69.rfc.like(likesrch), DataArt69.razon_social.like(likesrch))).order_by(
            DataArt69.rfc.asc(), DataArt69.fech_prim_pub.desc()).all()
    return render_template('index.html', title='Inicio', form=frmss, resp=(a69b, a69), fchs=updates)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    frm_lgin = LoginForm()
    if frm_lgin.validate_on_submit():
        user = User.query.filter_by(email=frm_lgin.username.data).first()
        if user is None or not user.check_password(frm_lgin.password.data):
            flash('Nombre de usuario o password invalido')
            return redirect(url_for('login'))
        login_user(user, remember=frm_lgin.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Ingreso', form=frm_lgin)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(fullname=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.new_id()
        wappdb.session.add(user)
        wappdb.session.commit()
        flash('Se ha registrado el usuario nuevo.')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/usuarios')
@login_required
def usuarios():
    if current_user.level == 0:
        u = User.query.all()
        return render_template('usuarios.html', title='Usuarios', users=u)
    else:
        return redirect(url_for('index'))


@app.route('/perfil/<iduser>', methods=['GET', 'POST'])
@app.route('/perfil', defaults={'iduser': None}, methods=['GET', 'POST'])
@app.route('/perfil/', defaults={'iduser': None}, methods=['GET', 'POST'])
@login_required
def perfil(iduser):
    cipher_text = iduser.encode("ISO-8859-1")
    iduser = decrypt_id(cipher_text)
    if not (str(iduser) == str(current_user.id) or str(current_user.level) == '0'):
        return redirect(url_for('index'))
    usr = User.query.filter_by(id=iduser).first_or_404()
    frm = EditProfileForm(usr.fullname, usr.email)
    frm.username.id = str(usr.fullname).replace(' ', '_')
    frm.email.id = usr.email
    if frm.validate_on_submit():
        user = User.query.filter_by(email=frm.original_email).first()
        user.fullname = frm.username.data
        user.email = frm.email.data
        if frm.oldpassword.data != '':
            user.set_password(frm.newpassword.data)
        wappdb.session.commit()
        flash('Actualización Exitosa.')
        return redirect(url_for('index'))
    return render_template('perfil.html', user=usr, form=frm)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Revise su correo electrónico para obtener las instrucciones para restablecer su contraseña')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Restablecer Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        wappdb.session.commit()
        flash('Su contraseña ha sido restablecida.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/dltusr/<iduser>', methods=['GET', 'POST'])
@app.route('/dltusr', defaults={'iduser': None}, methods=['GET', 'POST'])
@app.route('/dltusr/', defaults={'iduser': None}, methods=['GET', 'POST'])
@login_required
def dltusr(iduser):
    if current_user.level == 0:
        cipher_text = iduser.encode("ISO-8859-1")
        iduser = decrypt_id(cipher_text)
        if current_user.level != 0:
            return redirect(url_for('index'))
        usr = User.query.filter_by(id=iduser).first()
        wappdb.session.delete(usr)
        wappdb.session.commit()
    return redirect(url_for('usuarios'))


@app.template_filter('strftime')
def _jinja2_filter_datetime(dat, fmt=None):
    locale.setlocale(locale.LC_ALL, 'Spanish_Mexico')
    fechadt = dat
    format='%d de %B de %Y'
    return fechadt.strftime(format)
