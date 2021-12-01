#!/usr/bin/env python
from flask import Flask, render_template, flash
from flask import request,  Response

from flask import session, redirect
from flask.helpers import url_for

#import src.forms as forms
from src.correos import send_book_table, conf_email, cancel_book_table

## librerias de Mongodb
from flask.wrappers import Response
from flask_pymongo import PyMongo
import bcrypt

from datetime import datetime


app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb+srv://Alberto:Beto.mata8@cluster0.xzfip.mongodb.net/mydb?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://localhost/Basho"
mongo = PyMongo(app)
db= mongo.db
app.secret_key = "any random string"

resev_people = [{'value':'1 persona'}, {'value':'2 personas'}, {'value':'3 personas'}, {'value':'4 personas'}, {'value':'5 personas'}, {'value':'6 personas'}, {'value':'7 personas'}]
Horas = [{'hora':'4 pm'},{'hora':'5 pm'},{'hora':'6 pm'},{'hora':'7 pm'},{'hora':'8 pm'},{'hora':'9 pm'},{'hora':'10 pm'},]

@app.route('/')
def index():
    #Sacar eventos de la base de datos
    events = mongo.db.events
    AllEvents= events.find()
    #Agregar datos a la base de datos
    #events.insert_one({"title":"Navidad","description":"Felices fiestas a todos, comparti un barco con un diez porciento de descuento ","date":"24/12/2021","time":"7:00AM - 12:00PM"})
    # for document in AllEvents:
    #     print(document['title'])
    entradas = mongo.db.entradas
    AllEntradas= entradas.find()

    ensaladas = mongo.db.ensaladas
    AllEnsaladas= ensaladas.find()

    sushis = mongo.db.sushis
    AllSushis= sushis.find()

    postres = mongo.db.postres
    AllPostres= postres.find()

    footer = mongo.db.footer
    AllFooter= footer.find_one()
    #footer.insert_one({"DiasAlmuezo":"Martes-Domingo", "HorarioAlmuerzo":"10:30AM-3:00PM","DiasCena":"Martes-Domingo", "HorarioCena":"4:30PM-10:00PM","DiasCerrado":"Lunes"})
    # postres.insert_one({"title":"Brownie con helados","precio":"₡ 2,400 ","impuesto":"₡ 2,640", "title2":"Postre del día","precio2":"₡ 2,100 ","impuesto2":"₡ 2,310"})
    

    reservation = mongo.db.reservation
    if 'username' in session:
        existing_reservation_username = reservation.find_one({'username' : session['username']})
        if existing_reservation_username is None:
            session['reservacion'] =  True
        else:
            session['reservacion'] =  False

        username = session['username']
        if session['reservacion']:
            reservacion = session['reservacion']
            return render_template("index.html",username=True,reservacion=True, UserID=username, resev_people=resev_people, Horas=Horas, AllEvents = AllEvents, AllEntradas = AllEntradas, AllEnsaladas = AllEnsaladas, AllSushis = AllSushis, AllPostres = AllPostres, AllFooter = AllFooter)
        else:
            return render_template("index.html",username=True,reservacion=False, UserID=username, resev_people=resev_people, Horas=Horas, AllEvents = AllEvents, AllEntradas = AllEntradas, AllEnsaladas = AllEnsaladas, AllSushis = AllSushis, AllPostres = AllPostres, AllFooter = AllFooter)

    else:
        return render_template("index.html",username=False, AllEvents = AllEvents, AllEntradas = AllEntradas, AllEnsaladas = AllEnsaladas, AllSushis = AllSushis, AllPostres = AllPostres, AllFooter = AllFooter)

@app.route('/logout')
def logout():
    session.pop('username')
    flash("Ha finalizado sesión!")
    return redirect(url_for('index'))
    

@app.route('/mas')
def mas():
    footer = mongo.db.footer
    AllFooter= footer.find_one()

    galeria = mongo.db.galeria
    AllGaleria= galeria.find()
    #galeria.insert_one({"Title":" Arroz Goham", "Image":"arrozgohan.jpg"})
    
    historia = mongo.db.historia
    AllHistoria= historia.find_one()
    #historia.insert_one({"Description":" On her way she met a copy. The copy warned the Little Blind Text, that where it came from it would have been rewritten a thousand times and everything that was left from its origin would be the word "and" and the Little Blind Text should turn around and return to its own, safe country. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.On her way she met a copy. The copy warned the Little Blind Text, that where it came from it would have been rewritten a thousand times and everything that was left from its origin would be the word "and" and the Little Blind Text should turn around and return to its own, safe country. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.", "Image":"historia.jpg"})
    
    blog = mongo.db.blog
    AllBlog= blog.find()
    # blog.insert({"name":" Rolando Martines", "description":" Excelente atención y servicio", "image":"person_2.jpg"})

    return render_template("mas.html",AllFooter = AllFooter, AllGaleria=AllGaleria, AllHistoria = AllHistoria, AllBlog = AllBlog)

@app.route('/login', methods=['GET','POST'])
def login():
    users = mongo.db.users
    
    if request.method == 'POST': 
        login_user = users.find_one({'username' : request.form['username']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                flash("Ha iniciado sesión!")
                return redirect(url_for('index'))
            else:
                flash("Contraseña incorrecta")
                login_user['password'] = ""
                return render_template("login_wtf.html",userremember= request.form['username'] )
        else:
            print("Datos no validos")
            flash("Datos no validos")

    return render_template("login_wtf.html",userremember=  " ")


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST' :
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})
        existing_email = users.find_one({'email' : request.form['email']})
        print("Valido!")
        if request.form['username'] != "" and request.form['email']  != "" and request.form['lastname'] != "" and request.form['password'] != "" and request.form['confirm'] != "":
            if existing_user is None:
                if existing_email is None:
                    if request.form['password'] == request.form['confirm']:
                        hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                        hashpass2 = bcrypt.hashpw(request.form['confirm'].encode('utf-8'), bcrypt.gensalt())
                        users.insert({'name':request.form['name'],'username':request.form['username'], 'password': hashpass, 'email':request.form['email'],'lastname':request.form['lastname'], 'confirm': hashpass2})
                        session['username'] =  request.form['username']
                        try:
                                conf_email(request.form['username'], request.form['email'])
                        except:
                                print("Error en el correo")
                        return redirect(url_for('index'))
                    else:
                        flash("Confirmación de contraseña incorrecta")
                        print("Contraseña y contraseña de confirmación distintas")
                else:
                    flash("Email ya en sistema")
                    print("Email ya en sistema")    
            else:
                flash("Usuario ya en sistema")
                print("Usuario ya en sistema")
        else:
            flash("Porfavor completar todos los espacios")
            print("Porfavor completar todos los espacios")
    else:
        print("No válido!")

    return render_template("register_form.html")




@app.route('/get_reservation', methods=['GET','POST'])
def get_reservation():
   if request.method == 'POST':
        # Extraer data de pagina
        people = request.form.get('people')
        hora = request.form.get('Hora_select')
        date = request.form.get('select_date')
        now = datetime.now()
        if date is None:
             date = now
        else:
             date = datetime(int(date.split("/")[2]),int(date.split("/")[0]),int(date.split("/")[1]))

        # Obtener información del usuario
        users = mongo.db.users
        existing_user = users.find_one({'username' : session['username']})
        username= existing_user['username']
        email= existing_user['email']
        # Inicializar clase de reservación
        reservation = mongo.db.reservation

        existing_reservation_username = reservation.find_one({'username' : session['username']})
        existing_reservation_datehour = reservation.find_one({'date' : date,'hora' : hora})

        if date.date()>=now.date():
             if existing_reservation_username is None:
                 if existing_reservation_datehour is None:
                      # Mandar correo de confirmación
                      send_book_table(username, people, date.date(), hora, email)
                      # Actualizar base de datos
                      reservation.insert({'username':username,'email':email, 'date':date,'people':people, 'hora': hora})
                      flash("Reservación éxitosa")
                      session['reservacion'] =  False
                 else:
                      flash("Reservación fallida, espacio ocupado")

             else:
                  flash("Solo puede reservar 1 vez")
        else:
            flash("Fecha no disponible")

        return redirect(url_for('index'))
   else: 
        session['reservacion'] =  False
        reservation = mongo.db.reservation
        existing_reservation = reservation.find_one({'username' : session['username']})
        usuario= existing_reservation['username']
        people= existing_reservation['people']
        date= existing_reservation['date']
        hora= existing_reservation['hora']
        email= existing_reservation['email']
        cancel_book_table(usuario, people, date.date(), hora, email)
        reservation.delete_one({'username' : session['username']})
        flash("Su reservacion fue cancelada")
        session.pop('reservacion')
        return redirect(url_for('index'))

    

if __name__=='__main__':
    app.run(debug=True, port = 2000)