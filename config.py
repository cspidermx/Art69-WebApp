# import vars
# import cx_Oracle
import os
basedir = os.path.abspath(os.path.dirname(__file__))


def buildconnstring():
    pass
    # DBCRED = {'dburl': os.environ['DB_URL'] or 'URL-de-la-base',
    #           'dbport': os.environ['DB_PORT'] or 'PUERTO-de-la-base',
    #           'dbservice': os.environ['DB_SERVICE'] or 'SERVICENAME-de-la-base',
    #           'dbuser': os.environ['DB_USER'] or 'USER-de-la-base',
    #           'dbpass': os.environ['DB_PASS'] or 'PASS-de-la-base'}
    # dnsStr = cx_Oracle.makedsn(DBCRED['dburl'], DBCRED['dbport'], DBCRED['dbservice'])
    # dnsStr = dnsStr.replace('SID', 'SERVICE_NAME')
    # connect_str = 'oracle://' + DBCRED['dbuser'] + ':' + DBCRED['dbpass'] + '@' + dnsStr
    # return connect_str


class VarConfig(object):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = buildconnstring()
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