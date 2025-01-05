from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
import pytz
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_migrate import Migrate

########################################################################################
##################               DATA BASE                 #############################
########################################################################################
#flask db init
#flask db migrate -m "Descripción de los cambios"
#flask db upgrade

# Configuración de la aplicación
app = Flask(__name__)
app.secret_key = "Habits2025"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
# Start SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)


########################################################################################
##################               MODELS                 ################################
########################################################################################

# Modelo de base de datos
# Model of database
from datetime import datetime
from sqlalchemy import func


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    code = db.Column(db.String(200), nullable=False, unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    miembros = db.relationship(
        'User',
        secondary='user_group',
        back_populates='groups'
    )

    def __init__(self, name, author_id, code):
        self.name = name
        self.author_id = author_id
        self.code = code


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    private = db.Column(db.Boolean, nullable=False, default=True)
    name = db.Column(db.String(150), nullable=True, unique=False)
    last_name = db.Column(db.String(150), nullable=True, unique=False)

    groups = db.relationship(
        'Groups',
        secondary='user_group',
        back_populates='miembros'
    )

    def __init__(self, username, password):
        self.username = username
        self.password = password


user_group = db.Table(
    'user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)

bogota_tz = pytz.timezone("America/Bogota")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(bogota_tz))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    private = db.Column(db.Boolean, nullable=False, default=True)
    user = relationship('User', backref='tasks')

    def __repr__(self):
        return f"<Task {self.name}>"

    
class TaskDaily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idTask = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship(Task, backref='dailies', lazy=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(bogota_tz))

    def __repr__(self):
        return f"<TaskDaily {self.idTask}>"
