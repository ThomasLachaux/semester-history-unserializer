from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import etuutt
from os import environ

engine = create_engine(environ.get('DESTINATION_DATABASE'), echo=True, future=True)

Base = declarative_base()

class Mapping(Base):
  __tablename__ = 'mapping'

  id = Column(String(64), primary_key=True)
  user_id = Column(String(64))
  ue = Column(String(64))
  semester = Column(String(64))
  branch = Column(String(64))
  level = Column(String(64))
  faculty = Column(String(64))
  formation = Column(String(64))

Mapping.__table__.drop(engine, checkfirst=True)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()

i = 0
for user in etuutt.extract_data():
  for semesterId, semester in user['history'].items():
    for ue in semester['uvs'].values():
      # The space for Autditor Libre is important (in the data it's like this)
      if (ue 
        and semester['formation'] not in [None, 'Nc', 'Doctorat', 'Auditeur libre ', 'These']
        and semester['niveau'] not in ['2I1']):
        print(f'{user["id"]} - {i}')
        entity = Mapping(
          id = i, 
          user_id = user['id'], 
          ue = ue, 
          semester = semesterId, 
          branch = semester.get('branch', None), 
          level = semester['niveau'],
          faculty = semester.get('filiere', None),
          formation = semester['formation'])
        session.add(entity)
        i += 1
  
session.commit()
