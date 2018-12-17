# http://omawww.sat.gob.mx/cifras_sat/Paginas/datos/vinculo.html?page=ListCompleta69B.html
# http://omawww.sat.gob.mx/cifras_sat/Paginas/datos/vinculo.html?page=ListCompleta69.html
import urllib.request
import urllib.error
import time
import locale
import os
from webworker.models import Info69b, DataArt69b, HistoricArt69b, Info69, DataArt69
from sqlalchemy.sql.expression import func
from datetime import datetime
from datetime import timedelta
from webworker import ART69BCSVURL, DBSESSION, ART69CSVURL
import csv
import re


def rfc_valido(rfctxt):
    rerfc = '[A-ZÑ&]{3,4}\d{6}[A-V1-9][A-Z1-9][0-9A]'
    validado = re.match(rerfc, rfctxt)

    if validado is None:  # Coincide con el formato general del regex?
        return False
    else:
        return True


def check69bdb(filename):
    dif = 0
    r = DBSESSION.query(func.max(Info69b.id)).one()
    if r[0] is not None:
        maxr = DBSESSION.query(Info69b).filter_by(id=r[0]).one_or_none()
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


def getfechafromfile(f):
    with open(f) as a69csv:
        a69csv.seek(0)
        read_csv = csv.reader(a69csv, delimiter=',')
        fchfile = datetime.strptime('01/01/1980', '%d/%m/%Y')
        firstline = True
        for row in read_csv:
            if not firstline:
                if row[4] != '':
                    fech = datetime.strptime(row[4], '%d/%m/%Y')
                    df = fchfile.date() - fech.date()
                    if df.total_seconds() < 0:
                        fchfile = fech
            else:
                firstline = False
    return fchfile


def check69db(filename):
    dif = 0
    r = DBSESSION.query(func.max(Info69.id)).one()
    fecha = getfechafromfile(filename)
    if r[0] is not None:
        maxr = DBSESSION.query(Info69).filter_by(id=r[0]).one_or_none()
        fchdb = maxr.fechaupdate
        dif = fchdb - fecha.date()
    if type(dif) is not timedelta:
        return 1, fecha.date()
    else:
        return dif.total_seconds(), fecha.date()


def getfile(url, filename):
    dl = False
    gf_i = 0
    print('Getting file...', filename)
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


def fnum(cual):
    filenum = "0001"
    if not os.path.exists('historical' + cual + 'csv'):
        os.mkdir('historical' + cual + 'csv')
    else:
        last = os.listdir('historical' + cual + 'csv')
        mx = int(filenum)
        for fln in last:
            if cual == '69b':
                newmx = int(fln[7:11]) + 1
            else:
                newmx = int(fln[6:10]) + 1
            if newmx > mx:
                rng = 4 - len(str(newmx))
                filenum = "".join("0" for ii in range(rng)) + str(newmx)
    return filenum


def archive69b():
    current_idinfo = DBSESSION.query(func.max(Info69b.id)).one_or_none()
    if current_idinfo[0] is not None:
        data = DBSESSION.query(DataArt69b).all()
        for rc in data:
            newrecord = HistoricArt69b(id=rc.id, id_info=rc.id_info, rfc=rc.rfc, nombre=rc.nombre,
                                       situacion=rc.situacion, numofi_presuncion=rc.numofi_presuncion,
                                       fechaofi_presuncion=rc.fechaofi_presuncion,
                                       numofi_desvirtuado=rc.numofi_desvirtuado,
                                       fechaofi_desvirtuado=rc.fechaofi_desvirtuado,
                                       numofi_definitivo=rc.numofi_definitivo,
                                       fechaofi_definitivo=rc.fechaofi_definitivo, numofi_sentfav=rc.numofi_sentfav,
                                       fechaofi_sentfav=rc.fechaofi_sentfav)
            DBSESSION.add(newrecord)
        DBSESSION.commit()
        DBSESSION.query(DataArt69b).delete()
        DBSESSION.commit()


def clean69():
    DBSESSION.query(DataArt69).delete()
    DBSESSION.query(Info69).delete()
    DBSESSION.commit()


def update69b():
    art69b_file = 'historical69bcsv/art69b_' + str(fnum('69b')) + '.csv'
    getfile(ART69BCSVURL, art69b_file)
    # art69b_file = 'historical69bcsv/art69b_0002.csv'
    d = check69bdb(art69b_file)
    if d != 0:
        archive69b()
        with open(art69b_file) as a69bcsv:
            a69bcsv.seek(0)
            read_csv = csv.reader(a69bcsv, delimiter=',')
            i = 0
            fecha = ''
            idinfo = None
            for row in read_csv:
                if i == 0:
                    fecha = datetime.strptime(row[0][row[0].find(' al ') + 4:], '%d de %B de %Y')
                    nfo = Info69b(fechaupdate=fecha)
                    nfo.new_id()
                    idinfo = nfo.id
                    DBSESSION.add(nfo)
                    DBSESSION.commit()
                elif i == 2:
                    headers = row
                    headers[0] = 'id'
                    while '' in headers:
                        headers.remove('')
                elif i >= 3:
                    if row[1] is not None and row[1] != '':  # check if row[1] has data
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
                        newrecord = DataArt69b(id=row[0], id_info=idinfo, rfc=row[1], nombre=row[2], situacion=row[3],
                                               numofi_presuncion=nogpr, fechaofi_presuncion=fogpr,
                                               numofi_desvirtuado=nogdv, fechaofi_desvirtuado=fogdv,
                                               numofi_definitivo=nogdf, fechaofi_definitivo=fogdf,
                                               numofi_sentfav=nogsf, fechaofi_sentfav=fogsf)
                        DBSESSION.add(newrecord)
                i += 1
            DBSESSION.commit()
            print('Art69b: ', fecha)
    else:
        os.remove(art69b_file)


def update69():
    art69_file = 'historical69csv/art69_' + str(fnum('69')) + '.csv'
    getfile(ART69CSVURL, art69_file)
    # art69_file = 'historical69csv/art69_0001.csv'
    d, fecha = check69db(art69_file)
    if d != 0:
        clean69()
        with open(art69_file) as a69csv:
            a69csv.seek(0)
            read_csv = csv.reader(a69csv, delimiter=',')
            i = 0
            idinfo = 0
            for row in read_csv:
                if i == 0:
                    headers = row
                    headers[0] = 'id'
                    while '' in headers:
                        headers.remove('')
                    nfo = Info69(fechaupdate=fecha)
                    nfo.new_id()
                    idinfo = nfo.id
                    DBSESSION.add(nfo)
                    DBSESSION.commit()
                else:
                    if row[0] is not None and row[0] != '' and rfc_valido(row[0]):
                        rfc = row[0]
                        r_s = row[1]
                        t_p = row[2]
                        sup = row[3]
                        fmat = '%d/%m/%Y'  # 16/02/2018
                        if row[4] is not None and row[4] != '':
                            fepripu = datetime.strptime(row[4], fmat)
                        else:
                            fepripu = row[4]
                            print(i)
                        monto = row[5]
                        if monto == '':
                            monto = None
                        else:
                            monto = float(monto.strip())
                        if row[6] is not None and row[6] != '':
                            fepu = datetime.strptime(row[6], fmat)
                        else:
                            fepu = row[6]
                        if fepu == '':
                            fepu = None
                        newrecord = DataArt69(id=i, id_info=idinfo, rfc=rfc, razon_social=r_s, tipo_persona=t_p,
                                              supuesto=sup, fech_prim_pub=fepripu, monto=monto, fech_pub=fepu)
                        DBSESSION.add(newrecord)
                i += 1
            DBSESSION.commit()
            prev_file_num = int(art69_file.split('/')[-1][6:10]) - 1
            rng = 4 - len(str(prev_file_num))
            filenum = "".join("0" for ii in range(rng)) + str(prev_file_num)
            art69_file_prev = 'historical69csv/art69_' + filenum + '.csv'
            os.remove(art69_file_prev)
            os.rename(art69_file, art69_file_prev)
        print('Art69: ', fecha)
    else:
        os.remove(art69_file)


def runrobot():
    locale.setlocale(locale.LC_ALL, 'Spanish_Mexico')
    ini = datetime.now()
    update69b()
    update69()
    fin = datetime.now()
    dta = fin - ini
    print(dta.total_seconds())
    DBSESSION.close()
