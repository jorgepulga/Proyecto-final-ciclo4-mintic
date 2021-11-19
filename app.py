from logging import NullHandler
from flask import Flask, render_template, flash, request, session, redirect, url_for
import os
from config import dev
from models import *
from config import dev
from flask_login import LoginManager, login_required, logout_user, current_user, login_user #esta forma importa correctamente, flask.ext.login no
from forms import *
import db
from db import *
from werkzeug.urls import url_parse
app= Flask(__name__)
app.config.from_object(dev)
#db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view= "login"
#sesion_iniciada=False
#Admin=False
lista_nicknames=[]
lista_peliculas=["Casa Oscura", "Chernobil", "Eternos Compañeros", 
"Luca", "Escape Room 2", "Sin Tiempo"]
lista_estrenos=["Fast and Furious 10", "Space Jam 2", "Dune"]
dict_peliculas={"Casa Oscura":{"Sinopsis":"Casa Oscura Sinopsis", "Duracion":"90min"},
                "Chernobil":{"Sinopsis":" Chernobil Sinopsis", "Duracion":"90min"},
                "Eternos Compañeros":{"Sinopsis":"Eternos Compañeros Sinopsis", "Duracion":"90min"},
                "Luca":{"Sinopsis":"Luca Sinopsis", "Duracion":"90min"},
                "Escape Room 2":{"Sinopsis":"Escape Room 2 Sinopsis", "Duracion":"90min"},
                "Sin Tiempo":{"Sinopsis":"Sin Tiempo Sinopsis", "Duracion":"90min"},
                "Fast and Furious 10":{"Sinopsis":"Fast and Furious 10 Sinopsis", "Duracion":"90min"},
                "Space Jam 2":{"Sinopsis":"Space Jam 2 Sinopsis", "Duracion":"90min"},
                "Dune":{"Sinopsis":"Dune Sinopsis", "Duracion":"90min"}
}
cod_reserva=0
adminList=["AdminCine@cinemark.com.co"]
usermail=""
reserva={}
userReservas=[]
def get_user(email):
    if checkUsuario(email) == email:
            return user
    return None

@login_manager.user_loader
def load_user(user_id):
    for user in lista_nicknames:
        if user.id == int(user_id):
            return user
    return None

@app.route('/')
def index():
    return render_template('Pagina-de-inicio.html')

@app.route('/registro/', methods=['GET', 'POST'])
def RegistroUsuarios():
    form=SignupForm()#instancia local
    if current_user.is_authenticated:
        return redirect('/profile/')
    if form.validate_on_submit():
        nombre=form.name.data
        apellido=form.last_name.data
        id=form.id.data
        fecha_na=form.fecha_na.data
        sexo=form.sexo.data
        tel=form.phone.data
        email=form.email.data
        pwd=form.pwd.data
        city=form.ciudad.data
        user= User(id, nombre, apellido,  fecha_na, sexo, email, city, tel, pwd)
        print(user.id, user.nombre, user.apellido, user.fecha_na, user.sexo, user.email, user.ciudad, user.tel, user.p_w_d, user.is_admin)
        insert=db.insUsuario(user.id, user.nombre, user.apellido, user.fecha_na, user.sexo, user.email, user.ciudad, user.tel, user.p_w_d, user.is_admin)
        if insert:
            print('registró')
        login_user(user, remember=True) 
        return redirect('/login/')  
        '''next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('regstro')
        return redirect(next_page)   '''
    print(form.errors)
    
        
    return render_template('REGISTRO.html', form=form)

def checking_password(password, p_w_d):
        return check_password_hash(password, p_w_d)

@app.route ('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('profile')
    loginform = LoginForm()
    if loginform.validate_on_submit():
        userP= db.checkUsuario(loginform.email.data)
        if userP is not None:
            if checking_password(userP[0][8], loginform.pwd.data):
                login_user(userP[0][5], remember=loginform.remember_me.data)
                if checking_password(userP[0][8], loginform.pwd.data):
                    next_page = request.args.get('next')
                    if not next_page or url_parse(next_page).netloc != '':
                        next_page= url_for('profile')
                        return redirect(next_page)
                
            else:
                return 'False'                
    return render_template('INICIAR-SESION.html', loginform=loginform)

@app.route('/admin_dash/')
@login_required
def admin_dash():
    global sesion_iniciada
    global Admin
    return 'bienvenido Admin'

@app.route('/profile/')
def PaginaUsuario():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return render_template('PAGINA-DE-USUARIO.html') 
    else:
        return redirect('/') 
    
@app.route('/settings/', methods=['GET', 'POST'])
@login_required
def Configuración():
    return 'Ha entrado a la configuración de su cuenta'

@app.route('/logout/', methods=['GET', 'POST'])
def Salir():
    logout_user()
    return redirect('/')
    
@app.route('/cartelera/', methods=['GET', 'POST'])
def CarteleraPeliculas():
    return render_template('CARTELERA.html')
    
    
@app.route('/<pelicula>/details/', methods=['GET', 'POST'])
def DetallePelicula(pelicula):
    if pelicula not in lista_peliculas and pelicula not in lista_estrenos:
        mensaje= f'Lo sentimos. En el momento no hay información disponible acerca de {pelicula}. '
        reserva=False
    elif pelicula in lista_estrenos:
        mensaje= f'{pelicula} estará disponible muy pronto en nuestras salas.'
        reserva=True
    elif pelicula in lista_peliculas:
        mensaje= f'{pelicula} ya se encuentra disponible en nuestras salas.'
        reserva=True
    
    return render_template('pelicula.html', pelicula=pelicula, dict_peliculas=dict_peliculas, mensaje=mensaje, reserva=reserva)
   

@app.route('/reservas/consulta/', methods=['GET', 'POST'])
@login_required
def consultarReserva():
    global userReservas
    message='Consulta de Reservas'
    return render_template('reservaConsulta.html', message=message, userReservas=userReservas)
        
@app.route ('/reservas/<titulo>/', methods=['GET', 'POST'])
@login_required
def Reservas(titulo):
    global cod_reserva
    mensaje2=""
    if titulo not in lista_peliculas:
        if titulo not in lista_estrenos:
            mensaje= f'Lo sentimos, {titulo} no se encuentra disponible para la reserva'
            emision=False
        else:
            mensaje= f'Lo sentimos, {titulo} aún no se encuentra disponible para la reserva'
            emision=False
    else:
        mensaje= f'¡Enhorabuena! {titulo} se encuentra disponible para la reserva.'
        emision=True
        cod_reserva+=1

            
    return render_template('hacerreserva.html',mensaje=mensaje, titulo=titulo, emision=emision, cod_reserva=cod_reserva, mensaje2=mensaje2)

@app.route('/payments/<cod_reserva>/<titulo>/',methods=['GET', 'POST'])
@login_required
def PasarelaPago(cod_reserva, titulo):
    global usermail
    global reserva
    global userReservas
    mensaje2=""
    message='Ha entrado a la pasarela de pago. Proceda a realizar su compra'
    if request.method=='POST':
            seats=request.form['numAsientos']
            medioPago=request.form.getlist('medioPago')
            if len(seats)>0 and seats!='0':
                    reserva['Codigo']=cod_reserva
                    reserva['Pelicula']=titulo
                    reserva['Asientos']=seats
                    reserva['Medio de pago']=medioPago
                    userReservas.append(reserva)
                    return redirect ('/paysuccess/')
            else:
                    mensaje2='Error. Por favor llene todos los campos.'                   

    return render_template('pasarela.html', message=message, mensaje2=mensaje2, titulo=titulo, cod_reserva=cod_reserva)

@app.route('/paysuccess/',methods=['GET', 'POST'])
@login_required
def pagoExitoso():
    global usermail
    global reserva
    global userReservas
    return render_template('pagoexitoso.html', reserva=reserva, userReservas=userReservas)
        
@app.route('/teatros/')
def teatros():
    
    return render_template('teatros.html')
    
@app.route('/teatros/formato/<formato>', methods=['GET'])
def formatocine(formato):
    input=formato
    output= db.FormatoTeatro(input)
    return render_template('formato.html', formato=formato,output=output)

@app.route('/teatros/ciudad/<ciudad>', methods=['GET'])
def teatrobusqueda(ciudad):
    input=ciudad
    output= db.CiudadTeatro(input)
    return render_template('teatrobusqueda.html', output=output,ciudad=ciudad)
    
@app.route('/quienes-somos/', methods=['GET'])
def quienessomos():
    return render_template('empresa.html')



if __name__=='__main__':
    app.run(debug=True)
    