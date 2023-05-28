from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = 'localhost' # IP del servidor de base de datos
app.config['MYSQL_USER'] = 'root' # IP del servidor de base de datos
app.config['MYSQL_PASSWORD'] = 'franco1848' # IP del servidor de base de datos
app.config['MYSQL_DB'] = 'asistencia' # IP del servidor de base de datos
mysql = MySQL(app)

#Settings
app.secret_key = 'mysecretkey'

@app.route('/pag_p')
def pag_p():
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM asistencia')
    data = cur.fetchall()  
    return render_template('index.html', asistencia = data)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        nombre_c = request.form['Nombre_completo']
        rut = request.form['Rut']
        correo = request.form['Correo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO asistencia (Nombre_completo, Rut, Correo) VALUES (%s, %s, %s)',
        (nombre_c, rut, correo))
        mysql.connection.commit()
        flash('Usuario agregado correctamente')
        return redirect(url_for('pag_p'))

@app.route('/edit_user/<id>')
def get_user(id):
    curse = mysql.connection.cursor()
    curse.execute('SELECT * FROM asistencia WHERE id = {0}'.format(id))
    data = curse.fetchall()
    return render_template('edit-user.html', user = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_user(id):
    if request.method == 'POST':

        nombreCompleto = request.form['Nombre_completo']
        Rut = request.form['Rut']
        correo = request.form['Correo']
        cur= mysql.connection.cursor()
        cur.execute("""
        UPDATE asistencia
        SET Nombre_Completo = %s,
            Rut = %s,
            Correo = %s
        WHERE id = %s
        """, (nombreCompleto, Rut, correo, id))
        mysql.connection.commit()
        flash('Usuario actualizado correctamente')
        return redirect(url_for('pag_p'))

@app.route('/delete_user/<string:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM asistencia WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('pag_p'))

if __name__ =='__main__':   
    app.run(port = 3000, debug = True)