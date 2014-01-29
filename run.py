#!venv/bin/python

from streams import app, db

db.create_all()
app.run(debug=True)
