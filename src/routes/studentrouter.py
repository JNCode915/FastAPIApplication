from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.params import Form
from src.models.StudentForm import StudentForm
from src.service.StudentService import StudentService
from sqlalchemy.orm import Session
from src.config.db import get_db

#Router for student-related endpoints

BASE_DIR = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

#home page for the student management system
@router.get("/home", response_class=HTMLResponse)
async def show_homepage(request: Request):
    return templates.TemplateResponse(
        name="home.html",
        context={"request": request, "title": "My FastAPI App"},
    )

#Display all student details
#Acts as a single page application, where all the student details are displayed in a table format
@router.get("/getallstudents", response_class=HTMLResponse)
def get_all_students(request: Request, db: Session = Depends(get_db)):
    student_service = StudentService(db)
    students = student_service.get_all_students()
    return templates.TemplateResponse(
        name="students_display.html",
        context={"request": request, "students": students},
    )

#Display form to add a new student
@router.get("/addstudent",response_class=HTMLResponse)
def add_student_form(request: Request):
    return templates.TemplateResponse(
        "student_add_details.html",
        {"request": request, "title": "Add Student", "student": None},
    )   

#for both add and update student, we can use the same endpoint and check if the student exists or not
@router.post("/addorupdatestudent", response_class=HTMLResponse)
def studentInfo(
    request: Request,
    data: StudentForm = Depends(StudentForm.as_form),
    student_id: int = Form(None),
    db: Session = Depends(get_db),
):
    # create student using the service
    student_service = StudentService(db)
    student = student_service.get_student(student_id) if student_id else None
    if student:
        # Update existing student
        student_service.update_student(
            student_id=student_id, name=data.name, age=data.age, grade=data.grade
        )
    else:
        # Create new student    
        student_service.create_student(name=data.name, age=data.age, grade=data.grade)

    students = student_service.get_all_students()
    return templates.TemplateResponse(
        "students_display.html",
        {
            "request": request,
            "title": "Student Details",
            "students": students,
        },
    )
     
#get the student details by student id
#and route to the student_add_details.html page with the student details
@router.get("/updatestudent/{student_id}", response_class=HTMLResponse)
def update_student_form(request: Request, student_id: int,db: Session = Depends(get_db)):
    student_service = StudentService(db)
    student = student_service.get_student(student_id)
    if not student:
        return templates.TemplateResponse(
            "get_student.html",
            {
                "request": request,
                "title": "Get Student",
                "error": f"Student with ID {student_id} was not found.",
            },
        )
    else:
        return templates.TemplateResponse(
            "student_add_details.html",
            {"request": request, "title": "Update Student", "student": student},
        ) 
# post endpoint to update the student details
@router.post("/updatestudent/{student_id}", response_class=HTMLResponse)
def update_student(
    request: Request,
    student_id: int,
    data: StudentForm = Depends(StudentForm.as_form),
    db: Session = Depends(get_db),
):
    student_service = StudentService(db)
    student = student_service.get_student(student_id)
    if student:
        updated_student = student_service.update_student(
            student_id, name=data.name, age=data.age, grade=data.grade
        )
    if not updated_student:
        return templates.TemplateResponse(
            "get_student.html",
            {
                "request": request,
                "title": "Get Student",
                "error": f"Student with ID {student_id} was not found.",
            },
        )
    else:
        students = student_service.get_all_students()
        return templates.TemplateResponse(
            "students_display.html",
            {
                "request": request,
                "title": "Student Details",
                "students": students,
            },
        )   

#get the student id and delete the student from the database and route to the students_display.html page with the updated student details
@router.get("/deletestudent/{student_id}", response_class=HTMLResponse)
def delete_student(request: Request, student_id: int, db: Session = Depends(get_db
)):
    student_service = StudentService(db)
    success = student_service.delete_student(student_id)
    if not success:
        return templates.TemplateResponse(
            "get_student.html",
            {
                "request": request,
                "title": "Get Student",
                "error": f"Student with ID {student_id} was not found.",
            },
        )
    else:
        students = student_service.get_all_students()
        return templates.TemplateResponse(
            "students_display.html",
            {
                "request": request,
                "title": "Student Details",
                "students": students,
            },
        )

#not used
#just a get endpoint to route to the get_student.html page to get the student details by student id
@router.get("/getstudent", response_class=HTMLResponse)
def get_student(request: Request):
    #student_service = StudentService(db)
    #student = student_service.get_student(student_id)
   
     return templates.TemplateResponse(
        "get_student.html",
        {"request": request, "title": "Get Student"}
     )

#not used
# a post end point to get the student details by student id and route to the student_add_details.html page with the student details
@router.post("/getstudent", response_class=HTMLResponse)
def get_student_by_id(request: Request, student_id: int = Form(...), db: Session = Depends(get_db)):
    student_service = StudentService(db)
    student = student_service.get_student(student_id)
    if student:
        return templates.TemplateResponse(
           "student_add_details.html",
            {
                "request": request,
                "title": "Student Details",
                "student": student,
            },
       )
    else:
        return templates.TemplateResponse(
            "get_student.html",
            {
                "request": request,
                "title": "Get Student",
                "error": f"Student with ID {student_id} was not found.",
            },
        )
