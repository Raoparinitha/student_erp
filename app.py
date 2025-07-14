from flask import Flask, render_template, request, redirect
from models import db, Student, Attendance, Marks
from utils import send_alert

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    return render_template('students.html', students=Student.query.all())

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    parent_contact = request.form['parent_contact']
    new_student = Student(name=name, parent_contact=parent_contact)
    db.session.add(new_student)
    db.session.commit()
    return redirect('/students')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    students = Student.query.all()
    if request.method == 'POST':
        student_id = request.form['student_id']
        total = int(request.form['total_classes'])
        attended = int(request.form['attended_classes'])
        percentage = (attended / total) * 100

        new_attendance = Attendance(student_id=student_id, total_classes=total, attended_classes=attended, percentage=percentage)
        db.session.add(new_attendance)
        db.session.commit()

        if percentage < 85:
            student = Student.query.get(student_id)
            send_alert(student.name, student.parent_contact, percentage)

        return redirect('/attendance')

    return render_template('attendance.html', students=students)

@app.route('/marks', methods=['GET', 'POST'])
def marks():
    students = Student.query.all()
    if request.method == 'POST':
        student_id = request.form['student_id']
        semester = request.form['semester']
        subject = request.form['subject']
        marks = int(request.form['marks'])

        new_mark = Marks(student_id=student_id, semester=semester, subject=subject, marks=marks)
        db.session.add(new_mark)
        db.session.commit()
        return redirect('/marks')

    return render_template('marks.html', students=students)

@app.route('/dashboard')
def dashboard():
    data = []
    students = Student.query.all()
    for s in students:
        student_data = {
            'name': s.name,
            'attendance': [a.percentage for a in s.attendance],
            'marks': {m.semester: [] for m in s.marks}
        }
        for m in s.marks:
            student_data['marks'][m.semester].append((m.subject, m.marks))
        data.append(student_data)
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
