import os
from flask import Flask, render_template
from flask_mysqldb import MySQL
app = Flask(__name__)
# Configuración de MySQL con las credenciales de Render
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'dpg-cv5hhsi3esus73atsp1g-a')  # Usaremos las variables de entorno
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'mydatabase_8prt_user')  # Asegúrate de usar tus credenciales
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'qqvZ0Cv4wJf539z9wGv04vBGJWUQKGmH')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'mydatabase_8prt')
mysql = MySQL(app)
# Función para obtener los empleados
def get_employees():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users")
    rows = cursor.fetchall()
    cursor.close()
    return rows
# Rutas de la aplicación
@app.route("/")
def home():
    """Página de inicio"""
    return render_template("index.html")  # Página de inicio
@app.route("/empleados")
@app.route("/empleados")
def read():
    """Consulta la base de datos y muestra los empleados en una tabla HTML"""
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        # Aquí consulta la base de datos, asegúrate de que la tabla 'users' existe
        cursor.execute("SELECT id, name FROM users")
        rows = cursor.fetchall()
        cursor.close()
        return render_template("empleados.html", employees=rows)  # Renderiza los empleados
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")  # Esto imprimirá el error en la consola de la aplicación
        return render_template("error.html", error=str(e))  # Página de error con el mensaje
if __name__ == "__main__":
    app.run(debug=True)
