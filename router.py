from fastapi import APIRouter, HTTPException

from models import JobApplication, JobApplicationCreate, JobApplicationUpdate
import services

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=JobApplication, status_code=201)
def create_application(data: JobApplicationCreate):
    return services.create_application(data)


@router.get("/", response_model=list[JobApplication])
def list_applications():
    return services.get_all_applications()


@router.get("/{application_id}", response_model=JobApplication)
def get_application(application_id: int):
    app = services.get_application(application_id)
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.put("/{application_id}", response_model=JobApplication)
def update_application(application_id: int, data: JobApplicationUpdate):
    app = services.update_application(application_id, data)
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.delete("/{application_id}", status_code=204)
def delete_application(application_id: int):
    if not services.delete_application(application_id):
        raise HTTPException(status_code=404, detail="Application not found")
