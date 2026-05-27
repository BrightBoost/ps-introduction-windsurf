from models import JobApplication, JobApplicationCreate, JobApplicationUpdate

_applications: list[JobApplication] = []
_next_id: int = 1


def create_application(data: JobApplicationCreate) -> JobApplication:
    global _next_id
    application = JobApplication(id=_next_id, **data.model_dump())
    _applications.append(application)
    _next_id += 1
    return application


def get_all_applications() -> list[JobApplication]:
    return _applications


def get_application(application_id: int) -> JobApplication | None:
    for app in _applications:
        if app.id == application_id:
            return app
    return None


def update_application(application_id: int, data: JobApplicationUpdate) -> JobApplication | None:
    for i, app in enumerate(_applications):
        if app.id == application_id:
            updated = app.model_copy(update=data.model_dump(exclude_unset=True))
            _applications[i] = updated
            return updated
    return None


def delete_application(application_id: int) -> bool:
    for i, app in enumerate(_applications):
        if app.id == application_id:
            _applications.pop(i)
            return True
    return False
