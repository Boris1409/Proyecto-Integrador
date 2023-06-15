import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('base_datos.db')
c = conn.cursor()

# Crear tabla para usuarios
c.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT,
              rut TEXT,
              correo TEXT,
              contraseña TEXT)''')

# Crear tabla para docentes
c.execute('''CREATE TABLE IF NOT EXISTS docentes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT,
              asignatura TEXT,
              correo TEXT,
              contraseña TEXT)''')

# Crear tabla para salas de clases
c.execute('''CREATE TABLE IF NOT EXISTS salas
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              numero INTEGER)''')

# Crear tabla para ramos
c.execute('''CREATE TABLE IF NOT EXISTS ramos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT,
              hora_inicio TEXT,
              hora_fin TEXT,
              sala_id INTEGER,
              docente_id INTEGER,
              asignatura TEXT,
              FOREIGN KEY (sala_id) REFERENCES salas(id),
              FOREIGN KEY (docente_id) REFERENCES docentes(id))''')

# Crear tabla para inscripciones
c.execute('''CREATE TABLE IF NOT EXISTS inscripciones
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              usuario_id INTEGER,
              ramo_id INTEGER,
              FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
              FOREIGN KEY (ramo_id) REFERENCES ramos(id))''')

# Crear tabla para asistencia
c.execute('''CREATE TABLE IF NOT EXISTS asistencia
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              usuario_id INTEGER,
              ramo_id INTEGER,
              fecha DATE,
              asistio INTEGER,
              FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
              FOREIGN KEY (ramo_id) REFERENCES ramos(id))''')

# Insertar usuarios con correos y contraseñas
usuarios_data = [
    ("Juan Perez", "12345678-9", "est1@est.com", "pass1"),
    ("María González", "98765432-1", "est2@est.com", "pass2"),
    ("Pedro Ramirez", "56789012-3", "est3@est.com", "pass3"),
    ("Ana López", "21098765-4", "est4@est.com", "pass4"),
    ("Luis Torres", "43210987-6", "est5@est.com", "pass5"),
    ("Carolina Herrera", "87654321-0", "est6@est.com", "pass6")
]

c.executemany("INSERT INTO usuarios (nombre, rut, correo, contraseña) VALUES (?, ?, ?, ?)", usuarios_data)

# Insertar docentes con correos y contraseñas
docentes_data = [
    ("Profesor Matemáticas", "Matematicas", "doc1@doc.com", "pass1"),
    ("Profesor Química", "Quimica", "doc2@doc.com", "pass2"),
    ("Profesor Física", "Fisica", "doc3@doc.com", "pass3"),
    ("Profesor Programación", "Programacion", "doc4@doc.com", "pass4")
]

c.executemany("INSERT INTO docentes (nombre, asignatura, correo, contraseña) VALUES (?, ?, ?, ?)", docentes_data)

# Insertar salas de clases
salas_data = [
    (1,),
    (2,)
]

c.executemany("INSERT INTO salas (numero) VALUES (?)", salas_data)

# Insertar ramos
ramos_data = [
    ("Matemáticas", "01:30", "23:59", 1, 1, "Matematicas"),  # Agregar el ID del docente correspondiente (1) antes del ID de la sala (1)
    ("Química", "10:45", "12:45", 1, 2, "Quimica"),  # Agregar el ID del docente correspondiente (2) antes del ID de la sala (1)
    ("Física", "08:30", "23:59", 2, 3, "Fisica"),  # Agregar el ID del docente correspondiente (3) antes del ID de la sala (2)
    ("Programación", "10:45", "12:45", 2, 4, "Programacion"),  # Agregar el ID del docente correspondiente (4) antes del ID de la sala (2)
]

c.executemany("INSERT INTO ramos (nombre, hora_inicio, hora_fin, sala_id, docente_id, asignatura) VALUES (?, ?, ?, ?, ?, ?)", ramos_data)

# Relacionar estudiantes con asignaturas
estudiante_asignatura_data = [
    (1, 1),  # Estudiante 1 inscrito en la asignatura 1 (Matemáticas)
    (1, 3),  # Estudiante 1 inscrito en la asignatura 3 (Física)
    (2, 2),  # Estudiante 2 inscrito en la asignatura 2 (Química)
    (3, 1),  # Estudiante 3 inscrito en la asignatura 1 (Matemáticas)
    (4, 2),  # Estudiante 4 inscrito en la asignatura 2 (Química)
    (5, 3),  # Estudiante 5 inscrito en la asignatura 3 (Física)
    (6, 4)   # Estudiante 6 inscrito en la asignatura 4 (Programación)
]

c.executemany("INSERT INTO inscripciones (usuario_id, ramo_id) VALUES (?, ?)", estudiante_asignatura_data)

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
