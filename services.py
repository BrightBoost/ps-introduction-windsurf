from models import JobApplication, JobApplicationCreate, JobApplicationUpdate, ApplicationStatus

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


def search_applications(query: str) -> list[JobApplication]:
    """Search job applications by company name or role (case-insensitive).

    Args:
        query: The string to search for in company name or role.

    Returns:
        A list of JobApplication objects where the company or role contains the query.
    """
    q = query.lower()
    return [app for app in _applications if q in app.company.lower() or q in app.role.lower()]


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


def toggle_favorite(application_id: int) -> JobApplication | None:
    """Toggle the favorite status of a job application.

    Args:
        application_id: The unique identifier of the application.

    Returns:
        The updated JobApplication with toggled favorite status, or None if not found.
    """
    for i, app in enumerate(_applications):
        if app.id == application_id:
            updated = app.model_copy(update={"favorite": not app.favorite})
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


# questionable variable names
def update_application_status(applications, application_id, status, notes=None):
    """Update the status of a job application.

    Args:
        applications: A list of application dictionaries.
        application_id: The unique identifier of the application to update.
        status: The new status to set. Must be one of "applied",
            "interviewing", "offer", or "rejected".
        notes: Optional notes to attach to the application.

    Returns:
        The updated application dictionary, or None if the application
        was not found or the status is invalid.
    """
    valid_statuses = ["applied", "interviewing", "offer", "rejected"]
    if status not in valid_statuses:
        return None
    
    for application in applications:
        if application["id"] == application_id:
            application["status"] = status
            if notes is not None:
                application["notes"] = notes
            return application
    
    return None


# intention: filter applications by status
def get_applications_by_status(apps: list[JobApplication], status: ApplicationStatus) -> list[JobApplication]:
    """Filter applications by their status.

    Args:
        apps: A list of JobApplication objects.
        status: The status to filter by.

    Returns:
        A list of JobApplication objects matching the given status.
    """
    result = []
    for app in apps:
        if app.status == status:
            result.append(app)
    return result


def get_application_summary() -> dict:
    """Generate a summary of all job applications.

    Returns:
        A dictionary containing total count, status breakdown,
        response rate, success rate, rejection rate, and most recent application.
    """
    total = len(_applications)
    if total == 0:
        return {
            "total": 0,
            "by_status": {status.value: 0 for status in ApplicationStatus},
            "response_rate": 0.0,
            "success_rate": 0.0,
            "rejection_rate": 0.0,
            "most_recent": None,
        }

    by_status = {status.value: 0 for status in ApplicationStatus}
    for app in _applications:
        by_status[app.status.value] += 1

    responded = by_status["interviewing"] + by_status["offer"] + by_status["rejected"]
    response_rate = responded / total if total > 0 else 0.0
    success_rate = by_status["offer"] / total if total > 0 else 0.0
    rejection_rate = by_status["rejected"] / total if total > 0 else 0.0

    most_recent = max(_applications, key=lambda app: app.applied_date)

    return {
        "total": total,
        "by_status": by_status,
        "response_rate": round(response_rate * 100, 2),
        "success_rate": round(success_rate * 100, 2),
        "rejection_rate": round(rejection_rate * 100, 2),
        "most_recent": most_recent,
    }