from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # En app se encuentra nuestro servidor web de Flask

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tareas.db' # Conexion bbdd con app

db = SQLAlchemy(app) # Cursor para la base de datos SQLite

class Tarea(db.Model):
    __tablename__ = "tarea"
    id = db.Column(db.Integer, primary_key=True) # Identificador unico de cada tarea (no puede haber dos tareas con el mismo id, por eso es primary key)
    contenido = db.Column(db.String(200)) # Contenido de la tarea, un texto de maximo 200 caracteres
    hecha = db.Column(db.Boolean) # Booleano que indica si una tarea está hecha o no

db.create_all() # Creacion de las tablas
db.session.commit() # Ejecucion de las tareas pendientes de la base de datos

@app.route('/' )
def home():
    todas_las_tareas = Tarea.query.all()  # Consultamos y almacenamos todas las tareas de la base de datos
    return render_template("index.html", lista_de_tareas=todas_las_tareas)

@app.route('/crear-tarea', methods=['POST'])
def crear():
    # tarea es un objeto de la clase Tarea (una instancia de la clase)
    tarea = Tarea(contenido=request.form['contenido_tarea'], hecha=False) # id no es necesario asignarlo manualmente, porque la primary key se genera automáticamente
    db.session.add(tarea)  # Añadir el objeto de Tarea a la base de datos
    db.session.commit() # Ejecutar la operacion pendiente de la base de datos
    return redirect(url_for('home'))  # Esto nos redirecciona a la funcion home()

@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    tarea = Tarea.query.filter_by(id=int(id)).delete() # Se busca dentro de la base de datos, aquel registro cuyo id coincida con el aportado por el parametrode la ruta. Cuando se encuentra se elimina
    db.session.commit() # Ejecutar la operacion pendiente de la base de datos
    return redirect(url_for('home')) # Esto nos redirecciona a la funcion home() y si todo ha ido bien, al refrescar, la tarea eliminada ya no aparecera en el listado

@app.route('/tarea-hecha/<id>')
def hecha(id):
    tarea = Tarea.query.filter_by(id=int(id)).first() # Se obtiene la tarea que se busca
    tarea.hecha = not(tarea.hecha) # Guardamos en la variable booleana de la tarea, su contrario
    db.session.commit()  # Ejecutar la operacion pendiente de la base de datos
    return redirect(url_for('home'))  # Esto nos redirecciona a la funcion home()

if __name__ == '__main__':
    app.run(debug=True ) # El debug=True hace que cada vez que reiniciemos el servidor o modifiquemos codigo, el servidor de Flask se reinicie solo
