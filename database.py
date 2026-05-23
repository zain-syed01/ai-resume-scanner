import os
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mysecretpassword@db:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit =False, autoflush=False, bind=engine)

Base = declarative_base()


#Defining the job application table schema

class JobApplication(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    date_applied = Column(Date, nullable=False)
    status = Column(String, default="Applied")  #Applied, Interviewing, Offered, Rejected
    job_url = Column(String, nullable=True)