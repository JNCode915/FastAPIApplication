from sqlalchemy.orm import Session
from src.models.StudentData import StudentData

#Service class for managing student data
class StudentService:

    def __init__(self, db_session: Session ):
        self.db_session = db_session

    #Get a student by ID
    def get_student(self, student_id):
        return self.db_session.query(StudentData).filter(StudentData.id == student_id).first()

    #get all students from the database
    def get_all_students(self):
        return self.db_session.query(StudentData).all()
    
    #Add a new student to the database
    def create_student(self, name, age, grade):
        new_student = StudentData(name=name, age=age, grade=grade)
        try:
            self.db_session.add(new_student)
            self.db_session.commit()
            self.db_session.refresh(new_student)
            return new_student
        except Exception:
            self.db_session.rollback()
            raise
    
    #Update a student in the database
    def update_student(self, student_id, name=None, age=None, grade=None):
        student = self.get_student(student_id)
        if not student:
            return None
        if name is not None:
            student.name = name
        if age is not None:
            student.age = age
        if grade is not None:
            student.grade = grade
        self.db_session.commit()
        return student

    #delete a student from the database
    def delete_student(self, student_id):
        student = self.get_student(student_id)
        if not student:
            return False
        self.db_session.delete(student)
        self.db_session.commit()
        return True
