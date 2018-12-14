import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


ART69BCSVURL = os.environ.get('ART69BCSVURL')
ART69CSVURL = os.environ.get('ART69CSVURL')
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
DBENGINE = create_engine(SQLALCHEMY_DATABASE_URI)
DBSESSION = sessionmaker(bind=DBENGINE)()
