import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Datos de los estudiantes
students_data = [
    ('student1@example.com', 'password1', 1, '8:00', '23:00', 'English'),
    ('student2@example.com', 'password2', 2, '6:00', '8:00', 'Physics'),
    ('student3@example.com', 'password3', 3, '13:00', '14:00', 'Math'),
    ('student4@example.com', 'password4', 4, '15:00', '16:00', 'Chemistry'),
    ('student5@example.com', 'password5', 5, '10:00', '12:00', 'Biology'),  # nuevo estudiante y sala
    ('student6@example.com', 'password6', 6, '14:00', '15:00', 'Computer Science'),  # nuevo estudiante y sala
]

# Datos de los docentes
docentes_data = [
    ('docente1@example.com', 'password1'),
]

for student_data in students_data:
    email, password, room_id, start_time, end_time, subject = student_data
    cursor.execute("INSERT INTO students (email, password) VALUES (?, ?)", (email, password))
    student_id = cursor.lastrowid
    cursor.execute("INSERT INTO classes (room_id, student_id, start_time, end_time, subject) VALUES (?, ?, ?, ?, ?)", 
                   (room_id, student_id, start_time, end_time, subject))

conn.commit()
conn.close()

