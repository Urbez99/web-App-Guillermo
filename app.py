import os
from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_DATABASE_HOST', 'localhost')
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)


# 🔹 Página de inicio
@app.route("/")
def home():
    return render_template("index.html")  # Asegúrate de que 'index.html' existe en 'templates/'


@app.route("/empleados")
def read():
    """Consulta la base de datos y muestra los empleados en una tabla HTML"""
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM users")  
        rows = cursor.fetchall()
        cursor.close()

        return render_template("empleados.html", employees=rows)

    except Exception as e:
        return f"<h3 style='color:red;'>Error en la base de datos:</h3><p>{str(e)}</p><a href='/'>Volver a Inicio</a>"



# 🔹 Iniciar Servidor
if __name__ == "__main__":
    app.run(debug=True)
