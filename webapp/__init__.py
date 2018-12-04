import logging
from buffsmtplogger import BufferingSMTPHandler
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from config import VarConfig
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
# from logging.handlers import SMTPHandler


app = Flask(__name__)
app.config.from_object(VarConfig)
wappdb = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
mail_handler = BufferingSMTPHandler(app.config['SMTP']['server'],
                                    app.config['SMTP']['port'],
                                    app.config['SMTP']['user'],
                                    'cbarajas@carantmx.com',
                                    'Falla en art69bWebApp',
                                    10)
mail_handler.level = logging.ERROR
# auth = (app.config['SMTP']['user'], app.config['SMTP']['password'])
# mail_handler = SMTPHandler(
#             mailhost=(app.config['SMTP']['server'], app.config['SMTP']['port']),
#             fromaddr='no-reply@' + app.config['SMTP']['server'],
#             toaddrs='cbarajas@carantmx.com', subject='Fall en robot SAP',
#             credentials=auth, secure=app.config['SMTP']['SSL'])
# mail_handler.setLevel(logging.ERROR)
app.logger.addHandler(mail_handler)
if app.config['LOG_TO_STDOUT']:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
else:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/art69b.log',
                                       maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Iniciado')


from webapp import routes, models, errors
