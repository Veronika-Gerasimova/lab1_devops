from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Конфигурация БД: в Docker используется Postgres, локально/в тестах — SQLite
DATABASE_URL = os.getenv("DATABASE_URL")
TESTING = os.getenv("TESTING", "0") == "1"

if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
elif TESTING:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


with app.app_context():
    db.create_all()

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
    """, students=[s.to_dict() for s in Student.query.order_by(Student.id).all()])

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
        db.session.add(Student(name=name))
        db.session.commit()
    return redirect(url_for("get_students_page"))

# API JSON (для тестов)
@app.route("/api/students", methods=["GET"])
def get_students_json():
    all_students = [s.to_dict() for s in Student.query.order_by(Student.id).all()]
    return jsonify(all_students), 200

@app.route("/api/students", methods=["POST"])
def add_student_json():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    student = Student(name=data["name"])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201

# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    try:
        # простая проверка соединения с БД
        db.session.execute(db.text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
    return jsonify({"status": "healthy", "db": db_status}), 200

if __name__ == "__main__":
    with open("flask.pid", "w") as f:
        f.write(str(os.getpid()))
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", "5000")), debug=False, use_reloader=False)

