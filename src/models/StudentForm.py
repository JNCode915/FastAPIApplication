from pydantic import BaseModel
from fastapi import Form

# Pydantic model for the Student form data
class StudentForm(BaseModel):
    name: str
    age: int
    grade: int

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        age: int = Form(...),
        grade: int = Form(...),
    ):
        return cls(name=name, age=age, grade=grade)