import sqlite3
from sqlite3 import Error

def conectar():
    dbname='cinema.db'
    conn= sqlite3.connect(dbname)
    return conn

#SQL Tabla de usuario#
def insUsuario(id, nom, ape, fna, sex, mail,city,phone, pwd, rol):
    try :
        conn = conectar()
        conn.execute("insert into usuario (id_usuario, nombre, apellido, fecha_na, sexo, mail, ciudad, rol, telefono, pwd) values(?,?,?,?,?,?,?,?,?,?)", (id, nom, ape, fna, sex, mail,city, rol,phone, pwd))
        conn.commit()
        conn.close()
        return True
    except Error as error :
        print ('Error: ',error)
        return False


def checkUsuario(mail):
    try : 
        conn= conectar()
        SQLstmt=f"select * from usuario where mail='{mail}';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error

def listUsuario():
   conn = conectar()
   cursor= conn.execute ("select * from usuario")
   print (cursor.fetchall())
   conn.close()

#SQJ Tabla de Reservas"
def insReserva(idr, idf, ids, idp, idu):
    try :
        conn = conectar()
        conn.execute("insert into reservas (id_reserva, id_funcion, id_ sala, id_pelicula, id_usuario) values(?,?,?)", (idr, idf, ids, idp, idu))
        conn.commit()
        conn.close()
    except Error as error :
        print (error)

def listReserva():
   conn = conectar()
   cursor= conn.execute ("select * from reservas")
   print (cursor.fetchall())
   conn.close()

def CiudadTeatro(id):
    conn = conectar()
    try : 
        conn= conectar()
        SQLstmt="select * from teatros where ciudad='"+id+"';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error

def FormatoTeatro(id):
    conn = conectar()
    try : 
        conn= conectar()
        SQLstmt="select * from teatros where formato='"+id+"';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error