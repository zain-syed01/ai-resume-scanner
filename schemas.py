from pydantic import BaseModel, HttpUrl
from datetime import date
from typing import Optional

class JobApplicationBase(BaseModel):
    company_name: str
    job_title: str
    date_applied: date
    status: Optional[str] = "Applied"
    job_url: Optional[str] = None



class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationResponse(JobApplicationBase):
    id: int
    
    
    class Config:
        from_attributes = True

        