from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, redirect, url_for



########################################################################################
##################               DATA BASE                 #############################
########################################################################################

# Configuración de la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
# Start SQLAlchemy
db = SQLAlchemy(app)


########################################################################################
##################               MODELS                 ################################
########################################################################################

# Modelo de base de datos
# Model of database
from datetime import datetime
from sqlalchemy import func

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Llave primaria
    name = db.Column(db.String(50), nullable=False)  # Campo obligatorio
    description = db.Column(db.String(120), nullable=False)  # Descripción obligatoria
    frequency = db.Column(db.Integer, nullable=False)  # Frecuencia obligatoria
    created_at = db.Column(db.DateTime, default=func.now())  # Fecha de creación automática

    def __repr__(self):
        return f"<Task {self.name}>"
    
class TaskDaily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idTask = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship(Task, backref='dailies', lazy=True)
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f"<TaskDaily {self.idTask}>"



########################################################################################
##################                  APP                 ################################
########################################################################################


# Ruta principal para listar tareas
# Main route to list tasks
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route("/create_lugar/<int:task_id>", methods=["POST"])
def create_lugar(task_id):
    # Obtener la tarea desde la base de datos
    # Get task of Data Base
    task = Task.query.get(task_id)
    if task:
        # Crear un nuevo TaskDaily (lugar) relacionado con la tarea
        # Create a new TaskDaily
        new_task_daily = TaskDaily(idTask=task.id)
        db.session.add(new_task_daily)
        db.session.commit()
        
        # Redirigir de vuelta a la página donde se muestran las tareas
        # Redirec home
        return redirect(url_for("index"))
    return "Tarea no encontrada", 404


# Ruta para crear una nueva tarea
# Route to create a new task
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        frequency = request.form['frequency']
        new_task = Task(name=name, description=description, frequency=int(frequency))
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


# Ruta para editar una tarea existente
# Route to edit an existing task
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.name = request.form['name']
        task.description = request.form['description']
        task.frequency = request.form['frequency']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)


# Ruta para eliminar una tarea
# Route to delete a task
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task = Task.query.get_or_404(id)
    
    TaskDaily.query.filter_by(idTask=task.id).delete()
    
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


# Punto de entrada
# Entry point
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usamos el puerto desde la variable de entorno

    with app.app_context():
        db.create_all()
        
    app.run(host='0.0.0.0', port=port)