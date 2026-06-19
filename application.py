#--------------Using Raw SQL-----------------#

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional

from database import get_db


class StudentModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    age: Optional[int] = None
    phone_number: Optional[str] = None


app = FastAPI()


@app.get("/")
def root():
    return {"message": "working properly"}


@app.get("/get_students/{student_id}", response_model=StudentModel)
def get_student(student_id: int, db: Session = Depends(get_db)):

    result = db.execute(
        text("SELECT * FROM students WHERE id = :id"),
        {"id": student_id}
    )
    
    student = result.mappings().first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found."
        )

    return {
        "message":"Query run succesfully.",
        "student_details":student
    }


@app.get("/all_students", response_model=list[StudentModel])
def get_all_students(db: Session = Depends(get_db)):

    result = db.execute(
        text("SELECT * FROM students")
    )

    return result.mappings().all()


@app.post("/add_student", response_model=StudentModel)
def add_student(student_details: StudentModel,
                db: Session = Depends(get_db)):

    if not all([
        student_details.name,
        student_details.age,
        student_details.phone_number
    ]):
        raise HTTPException(
            status_code=400,
            detail="name, age and phone_number are required."
        )

    db.execute(
        text("""
            INSERT INTO students(name, age, phone_number)
            VALUES (:name, :age, :phone)
        """),
        {
            "name": student_details.name,
            "age": student_details.age,
            "phone": student_details.phone_number
        }
    )

    db.commit()

    result = db.execute(
        text("""
            SELECT *
            FROM students
            WHERE phone_number = :phone
        """),
        {"phone": student_details.phone_number}
    )

    return result.mappings().first()


@app.patch("/update_student/{student_id}", response_model=StudentModel)
def update_student(student_id: int,
                   updates: StudentModel,
                   db: Session = Depends(get_db)):

    result = db.execute(
        text("SELECT * FROM students WHERE id = :id"),
        {"id": student_id}
    )

    student = result.mappings().first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found."
        )

    update_data = updates.model_dump(
        exclude_unset=True,
        exclude={"id"}
    )

    for field, value in update_data.items():

        db.execute(
            text(
                f"UPDATE students SET {field} = :value WHERE id = :id"
            ),
            {
                "value": value,
                "id": student_id
            }
        )

    db.commit()

    result = db.execute(
        text("SELECT * FROM students WHERE id = :id"),
        {"id": student_id}
    )

    return result.mappings().first()


@app.delete("/delete_student/{student_id}")
def delete_student(student_id: int,
                   db: Session = Depends(get_db)):

    result = db.execute(
        text("SELECT * FROM students WHERE id = :id"),
        {"id": student_id}
    )

    student = result.mappings().first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found."
        )

    db.execute(
        text("DELETE FROM students WHERE id = :id"),
        {"id": student_id}
    )

    db.commit()

    return {
        "message": "Student deleted successfully",
        "removed_student_id": student_id
    }