#!venv/bin/python

import csv
import sys
sys.path.insert(0, '../streams')

from streams import app, db
from streams.models import RQCategory, Requirement

def import_data(file):
  with open(file) as f:
    for line in csv.reader(f, delimiter=',', quotechar='"'):
      Requirement.create(
        description=line[2].rstrip(),
        project_id=sys.argv[2],
        category_id=RQCategory.query.filter(RQCategory.name == line[0]).one().id,
        external_id=line[1])

if __name__ == "__main__":
  import_data(sys.argv[1])
