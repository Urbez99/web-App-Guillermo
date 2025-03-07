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

@app.route('/add_employees')
def add_employees():
    try:
        # Crear empleados
        employee1 = Employee(name="Úrbez Modrego")
        employee2 = Employee(name="Ana Cris Ruiz")
        employee3 = Employee(name="Sergio Alfranca")
        
        # Agregar a la base de datos
        db.session.add_all([employee1, employee2, employee3])
        db.session.commit()

        return "Empleados añadidos correctamente"
    except Exception as e:
        db.session.rollback()  # Asegura que no haya problemas si hay un error
        return f"<h3 style='color:red;'>Error al agregar empleados:</h3><p>{str(e)}</p>"


if __name__ == "__main__":
    if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Obtiene el puerto dinámico de Render, si está disponible
    app.run(debug=True, host="0.0.0.0", port=port)  # Asegura que esté escuchando en el puerto correcto

