from flask import Flask, request, jsonify, render_template_string, redirect, url_for

app = Flask(__name__)

# список студентов
students = [
    {"id": 1, "name": "Иван Иванов"},
    {"id": 2, "name": "Петр Петров"},
    {"id": 3, "name": "Анна Смирнова"},
    {"id": 4, "name": "Валя Смирнова"},
    {"id": 5, "name": "Валя Смирнова"},
    {"id": 6, "name": "Валя Смирнова"},
    {"id": 7, "name": "Валя Смирнова"},
    {"id": 8, "name": "Валя Смирнова"}
]

# главная страница
@app.route("/")
def index():
    return render_template_string("""
    <html>
    <head>
        <title>Студенты</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; background: #f9f9f9; }
            h1 { color: #333; }
            .menu { margin-top: 20px; }
            a { display: inline-block; margin: 10px 0; padding: 10px 15px; 
                background: #007BFF; color: white; text-decoration: none; border-radius: 6px; }
            a:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>Система управления студентами</h1>
        <div class="menu">
            <a href="{{ url_for('get_students_page') }}">📋 Список студентов</a><br>
            <a href="{{ url_for('add_student_form') }}">➕ Добавить студента</a>
        </div>
    </body>
    </html>
    """)

# список студентов (HTML)
@app.route("/students", methods=["GET"])
def get_students_page():
    return render_template_string("""
    <html>
    <head>
        <title>Список студентов</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; background: #f9f9f9; }
            table { border-collapse: collapse; width: 60%; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
            th { background: #007BFF; color: white; }
            tr:nth-child(even) { background: #f2f2f2; }
            a { margin-top: 20px; display: inline-block; text-decoration: none; color: #007BFF; }
        </style>
    </head>
    <body>
        <h2>📋 Список студентов</h2>
        <table>
            <tr><th>ID</th><th>Имя</th></tr>
            {% for s in students %}
            <tr><td>{{ s.id }}</td><td>{{ s.name }}</td></tr>
            {% endfor %}
        </table>
        <a href="{{ url_for('index') }}">⬅ Назад</a>
    </body>
    </html>
    """, students=students)

# форма добавления студента
@app.route("/add-student", methods=["GET"])
def add_student_form():
    return render_template_string("""
    <html>
    <head>
        <title>Добавить студента</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; background: #f9f9f9; }
            form { display: flex; flex-direction: column; width: 300px; }
            label { margin: 5px 0; }
            input { padding: 8px; margin-bottom: 10px; }
            button { padding: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #218838; }
            a { margin-top: 20px; display: inline-block; text-decoration: none; color: #007BFF; }
        </style>
    </head>
    <body>
        <h2>➕ Добавить студента</h2>
        <form action="{{ url_for('add_student_form') }}" method="post">
            <label for="name">Имя студента:</label>
            <input type="text" id="name" name="name" required>
            <button type="submit">Добавить</button>
        </form>
        <a href="{{ url_for('index') }}">⬅ Назад</a>
    </body>
    </html>
    """)

# обработка добавления студента
@app.route("/add-student", methods=["POST"])
def add_student_form_post():
    name = request.form.get("name")
    if name:
        new_id = max(s["id"] for s in students) + 1 if students else 1
        students.append({"id": new_id, "name": name})
    return redirect(url_for("get_students_page"))

# API JSON (для тестов)
@app.route("/api/students", methods=["GET"])
def get_students_json():
    return jsonify(students), 200

@app.route("/api/students", methods=["POST"])
def add_student_json():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    new_id = max(s["id"] for s in students) + 1 if students else 1
    new_student = {"id": new_id, "name": data["name"]}
    students.append(new_student)
    return jsonify(new_student), 201

if __name__ == "__main__":
    import os
    with open("flask.pid", "w") as f:
        f.write(str(os.getpid()))
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)




