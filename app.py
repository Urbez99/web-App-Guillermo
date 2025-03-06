import os
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_DATABASE_HOST', 'localhost')  # Se toma del entorno, si no se encuentra se pone 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)  # Asegúrate de pasar la app a MySQL()

@app.route("/")
def main():
    return "Hola!" #Mensaje cambiado

@app.route('/how are you')
def hello():
    #Descripción de la actualización
    return 'Sergio ha traducido la página al español y ha puesto estilos!'

@app.route('/read from database')
def read():
    conn = mysql.connection  # Establecer la conexión con la BD
    cursor = conn.cursor()   # Crear el cursor

    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()  # Obtener todas las filas

    result = []
    for row in rows:
        # Cambio en los estilos
        result.append(f"<p style='color: blue; font-weight: bold; font-family: Arial; background-color: lightgray; padding: 5px; border-radius: 5px;'>{row[0]} - {row[1]}</p>")  # Formato: id - nombre

    cursor.close()  # Cerrar el cursor

    return "<br>".join(result)  # Mostrar cada empleado en una línea


if __name__ == "__main__":
    app.run(debug=True)  # Habilitamos debug para mayor facilidad en el desarrollo
