# http://omawww.sat.gob.mx/cifras_sat/Paginas/datos/vinculo.html?page=ListCompleta69B.html
import urllib.request
import urllib.error
import time
import locale
import os


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


locale.setlocale(locale.LC_ALL, 'Spanish_Mexico')
ART69CSVURL = os.environ.get('ART69CSVURL')
i = "0001"
if not os.path.exists('historicalcsv'):
    os.mkdir('historicalcsv')
else:
    last = os.listdir('historicalcsv')
    mx = int(i)
    for fln in last:
        newmx = int(fln[7:11]) + 1
        if newmx > mx:
            rng = 4 - len(str(newmx))
            i = "".join("0" for i in range(rng)) + str(newmx)
art69_file = 'historicalcsv/art69b_' + str(i) + '.csv'
getfile(ART69CSVURL, art69_file)
