from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')




@app.route('/sala/<int:sala_id>', methods=['GET', 'POST'])
def tomar_asistencia(sala_id):
    if request.method == 'POST':
        correo_base = request.form['correo']
        dominio_correo = request.form['dominio_correo']
        correo = correo_base + dominio_correo
        contraseña = request.form['contraseña']

        conn = sqlite3.connect('base_datos.db')
        c = conn.cursor()

        if dominio_correo == "@doc.com":
            # Verificar si el usuario es un docente
            c.execute("SELECT * FROM docentes WHERE correo = ? AND contraseña = ?", (correo, contraseña))
            docente = c.fetchone()

            if docente:
                # Obtener registros de asistencia para el docente y la sala
                c.execute("SELECT asistencia.id, usuarios.nombre, asistencia.fecha FROM asistencia INNER JOIN usuarios ON asistencia.usuario_id = usuarios.id INNER JOIN ramos ON asistencia.ramo_id = ramos.id WHERE ramos.sala_id = ? AND ramos.asignatura = ? ORDER BY asistencia.fecha DESC", (sala_id, docente[2]))
                registros = c.fetchall()

                return render_template('registros.html', registros_asistencia=registros, docente=docente[1], asignatura=docente[2])
            else:
                mensaje = "Credenciales incorrectas. Por favor, verifica tu correo y contraseña."
                return render_template('asistencia.html', mensaje=mensaje, mostrar_marcar_asistencia=False)

        elif dominio_correo == "@est.com":
            # Verificar si el usuario existe en la tabla de usuarios
            c.execute("SELECT id FROM usuarios WHERE correo = ? AND contraseña = ?", (correo, contraseña))
            usuario_id = c.fetchone()

            if usuario_id:
                # Verificar si hay clases en curso en la sala indicada
                c.execute("SELECT id, nombre, hora_inicio, hora_fin FROM ramos WHERE sala_id = ? AND hora_inicio <= time('now', 'localtime') AND hora_fin >= time('now', 'localtime')", (sala_id,))
                clase_actual = c.fetchone()

                if clase_actual:
                    ramo_id = clase_actual[0]

                    # Verificar si el usuario está inscrito en el ramo actual
                    c.execute("SELECT id FROM inscripciones WHERE usuario_id = ? AND ramo_id = ?", (usuario_id[0], ramo_id))
                    inscripcion_registrada = c.fetchone()

                    if inscripcion_registrada:
                        # Verificar si el usuario ya ha registrado asistencia en esta clase
                        c.execute("SELECT id FROM asistencia WHERE usuario_id = ? AND ramo_id = ? AND fecha = date('now')", (usuario_id[0], ramo_id))
                        asistencia_registrada = c.fetchone()

                        if asistencia_registrada:
                            mensaje = "Ya has registrado tu asistencia para esta clase."
                            return render_template('asistencia.html', mensaje=mensaje, mostrar_marcar_asistencia=True)

                        # Registrar asistencia del usuario
                        c.execute("INSERT INTO asistencia (usuario_id, ramo_id, fecha, asistio) VALUES (?, ?, date('now'), 1)", (usuario_id[0], ramo_id))
                        conn.commit()

                        clase_info = {
                            'nombre': clase_actual[1],
                            'hora_inicio': clase_actual[2],
                            'hora_fin': clase_actual[3],
                            'sala_id': sala_id,  # Agregado: incluir el ID de la sala
                        }

                        mensaje = "¡Asistencia registrada con éxito!"
                        return render_template('asistencia.html', mensaje=mensaje, clase_info=clase_info, mostrar_marcar_asistencia=True)

                    else:
                        mensaje = "No estás inscrito en este ramo."
                        return render_template('asistencia.html', mensaje=mensaje, mostrar_marcar_asistencia=True)

                else:
                    mensaje = "No hay clases en curso en esta sala en este momento."
                    return render_template('asistencia.html', mensaje=mensaje, mostrar_marcar_asistencia=True)
            else:
                mensaje = "Credenciales incorrectas. Por favor, verifica tu correo y contraseña."
                return render_template('asistencia.html', mensaje=mensaje, mostrar_marcar_asistencia=True)
        else:
            return render_template('asistencia.html', mostrar_marcar_asistencia=False)
    else:
        return render_template('asistencia.html', mostrar_marcar_asistencia=False)




@app.route('/sala/<int:sala_id>/registros')
def ver_registros(sala_id):
    conn = sqlite3.connect('base_datos.db')
    c = conn.cursor()
    c.execute("SELECT asistencia.id, usuarios.nombre, asistencia.fecha, docentes.nombre AS docente, ramos.asignatura FROM asistencia INNER JOIN usuarios ON asistencia.usuario_id = usuarios.id INNER JOIN ramos ON asistencia.ramo_id = ramos.id INNER JOIN docentes ON ramos.docente_id = docentes.id WHERE ramos.sala_id = ? ORDER BY asistencia.fecha DESC", (sala_id,))
    registros = c.fetchall()

    c.execute("SELECT docentes.nombre, ramos.asignatura FROM docentes INNER JOIN ramos ON docentes.id = ramos.docente_id WHERE ramos.sala_id = ? LIMIT 1", (sala_id,))
    docente_asignatura = c.fetchone()

    conn.close()

    return render_template('registros.html', registros_asistencia=registros, docente=docente_asignatura[0], asignatura=docente_asignatura[1])


@app.route('/borrar_asistencia/<int:asistencia_id>', methods=['POST'])
def borrar_asistencia(asistencia_id):
    conn = sqlite3.connect('base_datos.db')
    c = conn.cursor()

    # Obtener el sala_id antes de eliminar el registro de asistencia
    c.execute("SELECT ramos.sala_id FROM asistencia INNER JOIN ramos ON asistencia.ramo_id = ramos.id WHERE asistencia.id = ?", (asistencia_id,))
    sala_id_result = c.fetchone()

    if sala_id_result:
        sala_id = sala_id_result[0]
        # Eliminar el registro de asistencia
        c.execute("DELETE FROM asistencia WHERE id = ?", (asistencia_id,))
        conn.commit()
        conn.close()

        return redirect(url_for('ver_registros', sala_id=sala_id))
    else:
        # Manejar el caso cuando no se encuentra el registro de asistencia
        conn.close()
        return "Error: No se encontró el registro de asistencia."
    
@app.route('/docentes', methods=['GET', 'POST'])
def docentes():
    if request.method == 'POST':
        correo_base = request.form['correo']
        dominio_correo = request.form['dominio_correo']
        correo = correo_base + dominio_correo
        contraseña = request.form['contraseña']
        asignatura = request.form['asignatura']

        conn = sqlite3.connect('base_datos.db')
        c = conn.cursor()

        c.execute("SELECT * FROM docentes WHERE correo = ? AND contraseña = ?", (correo, contraseña))
        docente = c.fetchone()

        if docente:
            # Verificar si el docente enseña la asignatura ingresada
            c.execute("SELECT id FROM ramos WHERE asignatura = ? AND docente_id = ?", (asignatura, docente[0]))
            ramos_ids = c.fetchall()

            if ramos_ids:
                registros = []
                for ramo_id in ramos_ids:
                    # Obtener registros de asistencia para el docente y la asignatura
                    c.execute("SELECT asistencia.id, usuarios.nombre, asistencia.fecha FROM asistencia INNER JOIN usuarios ON asistencia.usuario_id = usuarios.id WHERE asistencia.ramo_id = ? ORDER BY asistencia.fecha DESC", (ramo_id[0],))
                    registros += c.fetchall()

                return render_template('registros.html', registros_asistencia=registros, docente=docente[1], asignatura=asignatura)

            else:
                mensaje = "No enseñas la asignatura ingresada."
                return render_template('docentes.html', mensaje=mensaje)
        else:
            mensaje = "Credenciales incorrectas. Por favor, verifica tu correo y contraseña."
            return render_template('docentes.html', mensaje=mensaje)
    else:
        return render_template('docentes.html')
    
@app.route('/sobre_nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


if __name__ == '__main__':
    app.run(debug=True)
