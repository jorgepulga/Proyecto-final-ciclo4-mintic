from logging import DEBUG

from peewee import SqliteDatabase


#Conectamos el modelo con la aplicación
import os
class dev():
    DEBUG=True
    SECRET_KEY=os.urandom(32)
    DATABASE={
        'name': 'db.sqlite3',
        'engine': 'peewee.SqliteDatabase'
    }