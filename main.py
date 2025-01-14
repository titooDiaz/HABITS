from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Task, TaskDaily, app
import pytz
import os
from itertools import groupby
from datetime import date

# passwords hash
from werkzeug.security import generate_password_hash

# impor forms
from forms import LoginForm, RegisterForm

# user is login?
def user_on_login():
    user_id = session.get('user_id')
    print('user_id', user_id)
    if not user_id:
        flash("Debes iniciar sesión para ver tus tareas.", "danger")
        return True
    return False


########################################################################################
##################                  APP                 ################################
########################################################################################
app.secret_key = "Habits2025"

# users manager

# Ruta de Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
        else:
            # Encriptar la contraseña
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect(url_for('login'))  # Redirigir a login después de registrarse
    return render_template('users/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        print(f"Username: {username}, Password: {password}")
        
        user = User.query.filter_by(username=username).first()

        if user:
            print(f"Usuario encontrado: {user.username}")  # Verifica que el usuario exista en la base de datos
            print("asd",user.password)
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Inicio de sesión exitoso.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Contraseña incorrecta.', 'danger')
        else:
            flash('Usuario no encontrado.', 'danger')

    return render_template('users/login.html', form=form)

# Ruta protegida (dashboard)
@app.route('/dashboard')
def dashboard():
    if user_on_login():
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    
    today = date.today()
    print(today)

    tasks=Task.query.filter_by(user_id=user_id).all()

    # Agrupar tareas diarias por fecha
    all_dailies = [daily for task in tasks for daily in task.dailies]

    # Ordenar y agrupar las tareas por fecha
    sorted_dailies = sorted(all_dailies, key=lambda x: x.created_at.date())
    tasks_by_date = {
        date: list(dailies)
        for date, dailies in groupby(sorted_dailies, key=lambda x: x.created_at.date())
    }

    # Formatear las fechas para el template
    tasks_by_date_formatted = {
        date.strftime("%d/%m/%Y"): dailies for date, dailies in tasks_by_date.items()
    }

    today = date.today()
    tasks_today = TaskDaily.query.filter(db.func.date(TaskDaily.created_at) == today).all()
    count_today = len(tasks_today)
    print(count_today)
    
    
    # Consulta las tareas del usuario
    tasks = Task.query.filter_by(user_id=user_id).all()

    # Filtrar las tareas diarias de cada tarea que sean solo de hoy
    tasks_today = []
    tasks_today_number =[]
    
    for task in tasks:
        todays_dailies = [daily for daily in task.dailies if daily.created_at.date() == today]
        tasks_today_number.append(len(todays_dailies))
    tasks=zip(tasks,tasks_today_number)
    
    context = {
        'tasks_by_date': tasks_by_date_formatted,
        'tasks': tasks,
        'today': today
    }
    return render_template("index.html", **context)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))



# Ruta principal para listar tareas
# Main route to list tasks
@app.route('/')
def index():
    if user_on_login():
        return redirect(url_for('login'))
    return redirect(url_for('login'))




@app.route("/create_lugar/<int:task_id>", methods=["POST"])
def create_lugar(task_id):
    if user_on_login():
        return redirect(url_for('login'))
    # Obtener la tarea desde la base de datos
    # Get task of Data Base
    user_id = session.get('user_id')
    task = Task.query.get(task_id)
    if task:
        # Crear un nuevo TaskDaily relacionado con la tarea
        # Create a new TaskDaily
        new_task_daily = TaskDaily(idTask=task.id)
        db.session.add(new_task_daily)
        db.session.commit()
        
        # Redirigir de vuelta a la página donde se muestran las tareas
        # Redirec home
        return redirect(url_for("dashboard"))
    return "Tarea no encontrada", 404


# Ruta para crear una nueva tarea
# Route to create a new task
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        user_id = session['user_id']
        
        name = request.form['name']
        description = request.form['description']
        frequency = request.form['frequency']
        new_task = Task(name=name, description=description, frequency=int(frequency), user_id=int(user_id))
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('dashboard'))
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
    return redirect(url_for('dashboard'))



# Punto de entrada
# Entry point
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usamos el puerto desde la variable de entorno

    with app.app_context():
        db.create_all()
        
    app.run(host='0.0.0.0', port=port)