import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de PostgreSQL con las credenciales de Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://root:NFNoEW92FIxEHd1BYDgS4YtRXeNUSkAi@dpg-cv5i3cij1k6c73d1si7g-a.frankfurt-postgres.render.com/mydatabase_ans5')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de SQLAlchemy
db = SQLAlchemy(app)

# Modelo de la base de datos (Tabla de empleados)
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

    # Añadir empleados a la base de datos si no existen
    if not Employee.query.first():  # Solo los añade si no hay empleados aún
        employees_to_add = [
            Employee(name="Úrbez Modrego"),
            Employee(name="Ana Cris Ruiz"),
            Employee(name="Sergio Alfranca")
        ]
        db.session.add_all(employees_to_add)
        db.session.commit()

# Rutas de la aplicación
@app.route("/")
def home():
    """Página de inicio"""
    return render_template("index.html")  # Página de inicio

@app.route("/empleados")
def read():
    """Consulta la base de datos y muestra los empleados en una tabla HTML"""
    try:
        # Consulta la tabla de empleados
        employees = Employee.query.all()
        return render_template("empleados.html", employees=employees)  # Renderiza los empleados

    except Exception as e:
        return f"<h3 style='color:red;'>Error en la base de datos:</h3><p>{str(e)}</p><a href='/'>Volver a Inicio</a>"

if __name__ == "__main__":
    app.run(debug=True)
