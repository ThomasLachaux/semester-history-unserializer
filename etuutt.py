from sqlalchemy import create_engine, text
import phpserialize
from os import environ

def extract_data():
  engine = create_engine(environ.get('SOURCE_DATABASE'), echo=True, future=True)

  with engine.connect() as connection:
    rows = connection.execute(text("SELECT id, login, semestersHistory FROM etu_users WHERE semestersHistory != 'a:0:{}'"))
    
    for row in rows:
      yield {
        'id': row.id,
        'history': phpserialize.loads(bytearray(row.semestersHistory, 'utf8'), decode_strings=True)
      }