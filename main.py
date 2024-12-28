from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuración de la aplicación
# Settings of APP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Modelo de base de datos
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Llave primaria
    name = db.Column(db.String(50), nullable=False)  # Campo obligatorio
    description = db.Column(db.String(120), unique=True, nullable=False)  # Correo único
    frequency = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<tasks {self.name}>"

# Rutas de la aplicación
# Routes of APP
@app.route('/')
def index():
    return f"tasks: {Tasks.query.all()}"

# Punto de entrada
# Entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)