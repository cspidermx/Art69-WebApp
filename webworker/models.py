from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.sql.expression import func
from webworker import DBSESSION

Base = declarative_base()


class Info69b(Base):
    __tablename__ = 'info_art69b'

    id = Column(Integer, primary_key=True)
    fechaupdate = Column(Date)

    def new_id(self):
        mx = DBSESSION.query(func.max(Info69b.id)).one()
        if mx[0] is not None:
            self.id = mx[0] + 1
        else:
            self.id = 1


class DataArt69b(Base):
    __tablename__ = 'sat_art69b'

    id = Column(Integer, primary_key=True)
    id_info = Column(Integer, primary_key=True)
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


class HistoricArt69b(Base):
    __tablename__ = 'historico_art69b'

    id = Column(Integer, primary_key=True)
    id_info = Column(Integer, primary_key=True)
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
        mx = DBSESSION.query(func.max(HistoricArt69b.id)).one()
        if mx[0] is not None:
            self.id = mx[0] + 1
        else:
            self.id = 1


class Info69(Base):
    __tablename__ = 'info_art69'

    id = Column(Integer, primary_key=True)
    fechaupdate = Column(Date)

    def new_id(self):
        mx = DBSESSION.query(func.max(Info69.id)).one()
        if mx[0] is not None:
            self.id = mx[0] + 1
        else:
            self.id = 1


class DataArt69(Base):
    __tablename__ = 'sat_art69'

    id = Column(Integer, primary_key=True)
    id_info = Column(Integer, primary_key=True)
    rfc = Column(String, nullable=False)
    razon_social = Column(String, nullable=False)
    tipo_persona = Column(String, nullable=False)
    supuesto = Column(String, nullable=False)
    fech_prim_pub = Column(Date, nullable=False)
    monto = Column(DECIMAL)
    fech_pub = Column(Date)

    def new_id(self):
        mx = DBSESSION.query(func.max(DataArt69.id)).one()
        if mx[0] is not None:
            self.id = mx[0] + 1
        else:
            self.id = 1
