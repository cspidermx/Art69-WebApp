import os


class VarConfig(object):
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nunca-lo-podras-adivinar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SMTP = {'user': os.environ['SMTP_USER'] or 'Usuario-de-SMTP',
            'password': os.environ['SMTP_PASS'] or 'Password-de-SMTP',
            'server': os.environ['SMTP_SRV'] or 'Servidor-de-SMTP',
            'port': os.environ['SMTP_PORT'] or 'Puerto-de-SMTP',
            'SSL': os.environ['SMTP_SSL'] or 'SSL-de-SMTP'}
    IMAP = {'user': os.environ['IMAP_USER'] or 'Usuario-de-IMAP',
            'password': os.environ['IMAP_PASS'] or 'Password-de-IMAP',
            'server': os.environ['IMAP_SRV'] or 'Servidor-de-IMAP',
            'port': os.environ['IMAP_PORT'] or 'Puerto-de-IMAP'}