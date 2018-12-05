from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.expression import func
from webworker import DBSESSION

Base = declarative_base()


class Info(Base):
    __tablename__ = 'info_art69b'

    id = Column(Integer, primary_key=True)
    fechaupdate = Column(Date)

    def new_id(self):
        mx = DBSESSION.query(func.max(Info.id)).one()
        if mx[0] is not None:
            self.id = mx[0] + 1
        else:
            self.id = 1


class DataArt69b(Base):
    __tablename__ = 'sat_art69b'

    id = Column(Integer, primary_key=True)
    rfc = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    situacion = Column(String, nullable=False)
    numofi_presuncion = Column(String, nullable=False)
    fechaofi_presuncion = Column(Date, nullable=False)
    numofi_desvirtuado = Column(String)
    fechaofi_desvirtuado = Column(Date)
    numofi_definitivo = Column(String)
    fechaofi_definitivo = Column(Date)
    numofi_sentfav = Column(String)
    fechaofi_sentfav = Column(Date)

    def new_id(self):
        mx = DBSESSION.query(func.max(DataArt69b.id)).one()
        if mx[0] is not None:
            self.id = mx[0] + 1
        else:
            self.id = 1

    def update(self, r, nm, st, np, fp, ndv, fdv, ndef, fdef, ns, fs):
        self.rfc = r
        self.nombre = nm
        self.situacion = st
        self.numofi_presuncion = np
        self.fechaofi_presuncion = fp
        self.numofi_desvirtuado = ndv
        self.fechaofi_desvirtuado = fdv
        self.numofi_definitivo = ndef
        self.fechaofi_definitivo = fdef
        self.numofi_sentfav = ns
        self.fechaofi_sentfav = fs


class DesvirtuadoArt69b(Base):
    __tablename__ = 'desvirtuado_art69b'

    id = Column(Integer, primary_key=True)
    id_art69 = Column(Integer, nullable=False)
    rfc = Column(String, nullable=False)
    nombre = Column(String, nullable=False)

    def new_id(self):
        mx = DBSESSION.query(func.max(DataArt69b.id)).one()
        if mx[0] is not None:
            self.id = mx[0] + 1
        else:
            self.id = 1