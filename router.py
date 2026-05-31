from fastapi import APIRouter, HTTPException, Query

from models import JobApplication, JobApplicationCreate, JobApplicationUpdate, ApplicationStatus
import services

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=JobApplication, status_code=201)
def create_application(data: JobApplicationCreate):
    return services.create_application(data)


@router.get("/", response_model=list[JobApplication])
def list_applications(status: ApplicationStatus | None = Query(default=None, description="Filter by application status")):
    if status:
        return services.get_applications_by_status(services.get_all_applications(), status)
    return services.get_all_applications()


@router.get("/{application_id}", response_model=JobApplication)
def get_application(application_id: int):
    app = services.get_application(application_id)
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.get("/status/{status}", response_model=list[JobApplication])
def get_applications_by_status(status: ApplicationStatus):
    applications = services.get_applications_by_status(services.get_all_applications(), status)
    if not applications:
        raise HTTPException(status_code=404, detail="No applications found with this status")
    return applications


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
