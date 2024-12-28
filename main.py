from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Configuración de la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
# Start SQLAlchemy
db = SQLAlchemy(app)

# Modelo de base de datos
# Model of database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Llave primaria
    name = db.Column(db.String(50), nullable=False)  # Campo obligatorio
    description = db.Column(db.String(120), nullable=False)  # Descripción obligatoria
    frequency = db.Column(db.Integer, nullable=False)  # Frecuencia obligatoria

    def __repr__(self):
        return f"<Task {self.name}>"

# Ruta principal para listar tareas
# Main route to list tasks
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

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
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Punto de entrada
# Entry point
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usamos el puerto desde la variable de entorno
    app.run(host='0.0.0.0', port=port)

    with app.app_context():
        db.create_all()
    app.run(debug=True)
    