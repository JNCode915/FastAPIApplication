from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Database model for the Student table
class StudentData(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    grade = Column(Integer, nullable=False)

    