#!venv/bin/python

from streams import app, db
from streams.models import RQCategory, Release

def populate_db():
  if not RQCategory.query.all():
    RQCategory.create(name='TES')
    RQCategory.create(name='TDS')
    RQCategory.create(name='TIC')
    RQCategory.create(name='TRS')

def add_data():
  Release.create(name='Release 0.1', date='3/31/14')
  Release.create(name='Release 0.2', date='4/14/14')
  Release.create(name='Release 0.3', date='4/28/14')
  Release.create(name='Release 0.4', date='5/12/14')
  Release.create(name='CDR', date='4/23/14')
  Release.create(name='Build 3', date='5/19/14')

if __name__ == "__main__":
  populate_db()
