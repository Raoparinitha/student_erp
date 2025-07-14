from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    parent_contact = db.Column(db.String(100))
    attendance = db.relationship("Attendance", backref="student")
    marks = db.relationship("Marks", backref="student")

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    total_classes = db.Column(db.Integer)
    attended_classes = db.Column(db.Integer)
    percentage = db.Column(db.Float)

class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    semester = db.Column(db.String(10))
    subject = db.Column(db.String(100))
    marks = db.Column(db.Integer)
