import os
from flask import Flask, render_template, request, redirect, url_for
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

@app.route("/add_employee", methods=["GET"])
def show_add_employee_form():
    """Muestra el formulario para añadir un nuevo empleado"""
    return render_template("add_employee.html")

@app.route("/add_employee", methods=["POST"])
def add_employee():
    """Recibe los datos del formulario y añade un nuevo empleado a la base de datos"""
    try:
        # Obtener el nombre del empleado del formulario
        name = request.form["name"]
        
        # Crear el nuevo empleado
        new_employee = Employee(name=name)
        
        # Agregarlo a la base de datos
        db.session.add(new_employee)
        db.session.commit()

        # Redirigir a la lista de empleados
        return redirect(url_for("read"))

    except Exception as e:
        db.session.rollback()  # Asegura que no haya problemas si hay un error
        return f"<h3 style='color:red;'>Error al agregar empleado:</h3><p>{str(e)}</p>"

@app.route("/show_delete_employee_form", methods=["GET"])
def show_delete_employee_form():
    """Muestra el formulario para eliminar un empleado"""
    try:
        # Obtener la lista de empleados
        employees = Employee.query.all()
        return render_template("delete_employee.html", employees=employees)
    except Exception as e:
        return f"<h3 style='color:red;'>Error al obtener empleados:</h3><p>{str(e)}</p>"

@app.route("/delete_employee", methods=["POST"])
def delete_employee():
    """Elimina el empleado seleccionado de la base de datos"""
    try:
        # Obtener el ID del empleado a eliminar
        employee_id = request.form["employee_id"]
        
        # Buscar al empleado en la base de datos
        employee_to_delete = Employee.query.get(employee_id)
        
        if employee_to_delete:
            db.session.delete(employee_to_delete)
            db.session.commit()
            return redirect(url_for("read"))  # Redirigir a la lista de empleados
        else:
            return "<h3 style='color:red;'>Empleado no encontrado.</h3>"
    
    except Exception as e:
        db.session.rollback()
        return f"<h3 style='color:red;'>Error al eliminar empleado:</h3><p>{str(e)}</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Obtiene el puerto dinámico de Render, si está disponible
    app.run(debug=True, host="0.0.0.0", port=port)  # Asegura que esté escuchando en el puerto correcto
