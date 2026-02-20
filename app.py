from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'students.db')

# open a connection (simple dev/demo approach)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    course TEXT
)
''')
conn.commit()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return render_template('index.html', students=data)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']
    cursor.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)", (name, email, course))
    conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']
    cursor.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?", (name, email, course, id))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
