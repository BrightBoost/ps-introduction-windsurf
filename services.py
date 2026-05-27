from models import JobApplication, JobApplicationCreate, JobApplicationUpdate

_applications: list[JobApplication] = []
_next_id: int = 1


def create_application(data: JobApplicationCreate) -> JobApplication:
    """Create a new job application and add it to the data store.

    Args:
        data: The job application data to create.

    Returns:
        The newly created JobApplication with an auto-generated id.
    """
    global _next_id
    application = JobApplication(id=_next_id, **data.model_dump())
    _applications.append(application)
    _next_id += 1
    return application


def get_all_applications() -> list[JobApplication]:
    """Retrieve all job applications.

    Returns:
        A list of all stored JobApplication objects.
    """
    return _applications


def get_application(application_id: int) -> JobApplication | None:
    """Retrieve a single job application by its id.

    Args:
        application_id: The unique identifier of the application.

    Returns:
        The matching JobApplication, or None if not found.
    """
    for app in _applications:
        if app.id == application_id:
            return app
    return None


def update_application(application_id: int, data: JobApplicationUpdate) -> JobApplication | None:
    """Update an existing job application with partial data.

    Args:
        application_id: The unique identifier of the application to update.
        data: The fields to update. Only provided fields are changed.

    Returns:
        The updated JobApplication, or None if not found.
    """
    for i, app in enumerate(_applications):
        if app.id == application_id:
            updated = app.model_copy(update=data.model_dump(exclude_unset=True))
            _applications[i] = updated
            return updated
    return None


def delete_application(application_id: int) -> bool:
    """Delete a job application by its id.

    Args:
        application_id: The unique identifier of the application to delete.

    Returns:
        True if the application was deleted, False if not found.
    """
    for i, app in enumerate(_applications):
        if app.id == application_id:
            _applications.pop(i)
            return True
    return False
