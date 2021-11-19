from app import *
@app.cli.command('crear_user')
def crear_user():
    db.init_app(app)
    u1=usuario.get_or_create(p_w_d='u1', nombre='u1', 
    apellido='rodriguez', fecha_na='2017-01-23', sexo='1', 
    mail='roberto1@gmail.com', ciudad='bogota', rol=0)
    print(u1)

app.cli()

