#!venv/bin/python
from os import environ

root_path = environ.get('STREAMS_DIR')

activate_this = '{0}/venv/bin/activate_this.py'.format(root_path)
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, root_path)

from streams import app as application
