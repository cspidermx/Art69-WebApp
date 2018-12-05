# http://omawww.sat.gob.mx/cifras_sat/Paginas/datos/vinculo.html?page=ListCompleta69B.html
import urllib.request
import urllib.error
import time
import locale
import os
from webworker.models import Info, DataArt69b
from sqlalchemy.sql.expression import func
from datetime import datetime
from datetime import timedelta
from webworker import ART69CSVURL, DBSESSION
import csv


def checkdb(filename):
    dif = 0
    r = DBSESSION.query(func.max(Info.id)).one()
    if r[0] is not None:
        maxr = DBSESSION.query(Info).filter_by(id=r[0]).one_or_none()
        fchdb = maxr.fechaupdate
        csvfile = open(filename)
        readfile = csv.reader(csvfile, delimiter=',')
        rwfch = readfile.__next__()
        fchfile = datetime.strptime(rwfch[0][rwfch[0].find(' al ') + 4:], '%d de %B de %Y')
        csvfile.close()
        dif = fchdb - fchfile.date()
    if type(dif) is not timedelta:
        return 1
    else:
        return dif.total_seconds()


def getfile(url, filename):
    dl = False
    gf_i = 0
    print('Getting file...')
    while not dl and gf_i < 10:
        try:
            print('Try #{}'.format(gf_i))
            urllib.request.urlretrieve(url, filename)
            dl = True
            print('Success!')
        except urllib.error.URLError as e:
            print(e.reason, " -- ", url)
            time.sleep(60)
            gf_i += 1


def getnum(data):
    if data.find('//') != -1:
        data = str(data).split('//')[-1]
    data = data.strip()
    if data.find('de fecha') != -1:
        return data[:data.find('de fecha') - 1]
    else:
        return data


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def dateconvert(dtafch, ln):
    err = ''
    done = False
    fmat = '%d de %B de %Y'
    fechadt = None
    if dtafch.find('//') != -1:
        dtafch = str(dtafch).split('//')[-1]
    if dtafch.find('de fecha') == -1:
        return None
    while not done:
        try:
            fstr = dtafch[dtafch.find('de fecha')+9:]
            for char in fstr:
                if char in "?":
                    fstr = fstr.replace(char, '')
            fstr = fstr.strip()
            if not(is_number(fstr[0]) and is_number(fstr[1])):
                fstr = '0' + fstr
            fechadt = datetime.strptime(fstr, fmat)
            done = True
        except ValueError as e:
            if err == '':
                err = '|' + ln + '|' + dtafch
            else:
                if len(dtafch) == 0:
                    print(err)
            # print(e, '|', ln, '|', dtafch, '|', dtafch[dtafch.find('de fecha') + 9:])
            if str(e).find('remains') != -1:
                dtafch = dtafch[:-1]
            else:
                if fmat == '%d %B %Y':
                    fmat = '%d de %B del %Y'
                else:
                    fmat = '%d %B %Y'
    return fechadt


def runrobot():
    locale.setlocale(locale.LC_ALL, 'Spanish_Mexico')
    filenum = "0001"
    if not os.path.exists('historicalcsv'):
        os.mkdir('historicalcsv')
    else:
        last = os.listdir('historicalcsv')
        mx = int(filenum)
        for fln in last:
            newmx = int(fln[7:11]) + 1
            if newmx > mx:
                rng = 4 - len(str(newmx))
                filenum = "".join("0" for ii in range(rng)) + str(newmx)
    art69_file = 'historicalcsv/art69b_' + str(filenum) + '.csv'
    getfile(ART69CSVURL, art69_file)

    d = checkdb(art69_file)
    if d != 0:
        with open(art69_file) as a69csv:
            a69csv.seek(0)
            read_csv = csv.reader(a69csv, delimiter=',')
            i = 0
            fecha = ''
            headers = ''
            for row in read_csv:
                if i == 0:
                    fecha = datetime.strptime(row[0][row[0].find(' al ') + 4:], '%d de %B de %Y')
                    nfo = Info(fechaupdate=fecha)
                    nfo.new_id()
                    DBSESSION.add(nfo)
                    DBSESSION.commit()
                elif i == 2:
                    headers = row
                    headers[0] = 'id'
                    while '' in headers:
                        headers.remove('')
                elif i >= 3:
                    nfogpr = row[4]
                    nfogdv = row[9]
                    nfogdf = row[11]
                    nfogsf = row[14]
                    nogpr = fogpr = nogdv = fogdv = nogdf = fogdf = nogsf = fogsf = None
                    if nfogpr != '':
                        nogpr = getnum(nfogpr)
                        fogpr = dateconvert(nfogpr, row[0])
                    if nfogdv != '':
                        nogdv = getnum(nfogdv)
                        fogdv = dateconvert(nfogdv, row[0])
                    if nfogdf != '':
                        nogdf = getnum(nfogdf)
                        fogdf = dateconvert(nfogdf, row[0])
                    if nfogsf != '':
                        nogsf = getnum(nfogsf)
                        fogsf = dateconvert(nfogsf, row[0])
                    existent = DBSESSION.query(DataArt69b).filter_by(id=row[0]).one_or_none()
                    if existent is not None:
                        existent.update(r=row[1], nm=row[2], st=row[3], np=nogpr, fp=fogpr, ndv=nogdv, fdv=fogdv,
                                        ndef=nogdf, fdef=fogdf, ns=nogsf, fs=fogsf)
                        DBSESSION.commit()
                    else:
                        newrecord = DataArt69b(row[0], row[1], row[2], row[3], nogpr, fogpr, nogdv, fogdv, nogdf, fogdf,
                                               nogsf, fogsf)
                        DBSESSION.add(newrecord)
                        DBSESSION.commit()
                i += 1
            print(fecha)
    else:
        os.remove(art69_file)

    DBSESSION.close()
