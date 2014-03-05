streams
=======

Development management tool

easy_install twill
pip install -r requirements.txt

After running pip make the following change:
Edit /usr/lib/python2.7/site-packages/migrate/changeset/ansisql.py
-from sqlalchemy.schema import SchemaVisitor
+from sqlalchemy.sql.base import SchemaVisitor

./db_migrate db init
./db_migrate db migrate
./db_migrate db upgrade
