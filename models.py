from peewee import *
from playhouse.flask_utils import FlaskDB
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#db=FlaskDB()


#\\\--------------------------------------User Model empieza aquí---------------------------------------///

class User(UserMixin):
    def __init__(self, id, nombre, apellido, fecha_na, sexo, email, ciudad, tel, p_w_d, is_admin=False):
        self.id = id
        self.nombre =nombre
        self.apellido=apellido
        self.email = email
        self.fecha_na=fecha_na
        self.sexo=sexo
        self.tel=tel
        self.ciudad=ciudad
        self.p_w_d = generate_password_hash(p_w_d)
        self.is_admin = is_admin
    def set_password(self, p_w_d):
        self.p_w_d = generate_password_hash(p_w_d)
    def check_password(self, p_w_d):
        return check_password_hash(self.p_w_d, p_w_d)
    def __repr__(self):
        return '<User {}>'.format(self.email)






