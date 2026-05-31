from datetime import date

import pytest

import services
from models import ApplicationStatus, JobApplicationCreate, JobApplicationUpdate


@pytest.fixture(autouse=True)
def reset_state():
    """Reset the in-memory state before each test."""
    services._applications = []
    services._next_id = 1
    yield


def test_create_application_adds_to_list_and_returns_correct_object():
    data = JobApplicationCreate(
        company="TechCorp",
        role="Software Engineer",
        status=ApplicationStatus.applied,
        applied_date=date(2024, 1, 15),
        notes="Great opportunity"
    )

    result = services.create_application(data)

    assert result.id == 1
    assert result.company == "TechCorp"
    assert result.role == "Software Engineer"
    assert result.status == ApplicationStatus.applied
    assert result.applied_date == date(2024, 1, 15)
    assert result.notes == "Great opportunity"
    assert len(services._applications) == 1
    assert services._applications[0] == result


def test_create_application_increments_id():
    data1 = JobApplicationCreate(
        company="Company A",
        role="Role A",
        status=ApplicationStatus.applied,
        applied_date=date(2024, 1, 1)
    )
    data2 = JobApplicationCreate(
        company="Company B",
        role="Role B",
        status=ApplicationStatus.interviewing,
        applied_date=date(2024, 1, 2)
    )

    result1 = services.create_application(data1)
    result2 = services.create_application(data2)

    assert result1.id == 1
    assert result2.id == 2
    assert len(services._applications) == 2


def test_get_application_by_id_returns_correct_application():
    data1 = JobApplicationCreate(
        company="Company A",
        role="Role A",
        status=ApplicationStatus.applied,
        applied_date=date(2024, 1, 1)
    )
    data2 = JobApplicationCreate(
        company="Company B",
        role="Role B",
        status=ApplicationStatus.interviewing,
        applied_date=date(2024, 1, 2)
    )
    app1 = services.create_application(data1)
    app2 = services.create_application(data2)

    result = services.get_application(app2.id)

    assert result == app2
    assert result.company == "Company B"


def test_get_application_by_id_returns_none_if_not_found():
    data = JobApplicationCreate(
        company="Company A",
        role="Role A",
        status=ApplicationStatus.applied,
        applied_date=date(2024, 1, 1)
    )
    services.create_application(data)

    result = services.get_application(999)

    assert result is None


def test_update_application_changes_status_and_notes():
    data = JobApplicationCreate(
        company="TechCorp",
        role="Software Engineer",
        status=ApplicationStatus.applied,
        applied_date=date(2024, 1, 15),
        notes="Initial notes"
    )
    app = services.create_application(data)

    update_data = JobApplicationUpdate(
        status=ApplicationStatus.interviewing,
        notes="Updated notes"
    )
    result = services.update_application(app.id, update_data)

    assert result is not None
    assert result.status == ApplicationStatus.interviewing
    assert result.notes == "Updated notes"
    assert result.company == "TechCorp"
    assert result.role == "Software Engineer"
    assert services._applications[0].status == ApplicationStatus.interviewing


def test_update_application_returns_none_if_not_found():
    update_data = JobApplicationUpdate(status=ApplicationStatus.offer)

    result = services.update_application(999, update_data)

    assert result is None


def test_delete_application_removes_from_list():
    data1 = JobApplicationCreate(
        company="Company A",
        role="Role A",
        status=ApplicationStatus.applied,
        applied_date=date(2024, 1, 1)
    )
    data2 = JobApplicationCreate(
        company="Company B",
        role="Role B",
        status=ApplicationStatus.interviewing,
        applied_date=date(2024, 1, 2)
    )
    app1 = services.create_application(data1)
    app2 = services.create_application(data2)

    result = services.delete_application(app1.id)

    assert result is True
    assert len(services._applications) == 1
    assert services._applications[0] == app2
    assert services.get_application(app1.id) is None


def test_delete_application_returns_false_if_not_found():
    result = services.delete_application(999)

    assert result is False


def test_get_applications_by_status_returns_only_matching():
    apps = [
        JobApplicationCreate(
            company="Company A",
            role="Role A",
            status=ApplicationStatus.applied,
            applied_date=date(2024, 1, 1)
        ),
        JobApplicationCreate(
            company="Company B",
            role="Role B",
            status=ApplicationStatus.interviewing,
            applied_date=date(2024, 1, 2)
        ),
        JobApplicationCreate(
            company="Company C",
            role="Role C",
            status=ApplicationStatus.applied,
            applied_date=date(2024, 1, 3)
        ),
        JobApplicationCreate(
            company="Company D",
            role="Role D",
            status=ApplicationStatus.offer,
            applied_date=date(2024, 1, 4)
        ),
    ]
    created_apps = [services.create_application(app) for app in apps]

    applied_apps = services.get_applications_by_status(
        services._applications, ApplicationStatus.applied
    )

    assert len(applied_apps) == 2
    assert all(app.status == ApplicationStatus.applied for app in applied_apps)
    assert created_apps[0] in applied_apps
    assert created_apps[2] in applied_apps


def test_get_applications_by_status_returns_empty_list_when_no_matches():
    apps = [
        JobApplicationCreate(
            company="Company A",
            role="Role A",
            status=ApplicationStatus.applied,
            applied_date=date(2024, 1, 1)
        ),
    ]
    services.create_application(apps[0])

    result = services.get_applications_by_status(
        services._applications, ApplicationStatus.rejected
    )

    assert result == []


def test_get_application_summary_returns_correct_data():
    apps = [
        JobApplicationCreate(
            company="Company A",
            role="Role A",
            status=ApplicationStatus.applied,
            applied_date=date(2024, 1, 1)
        ),
        JobApplicationCreate(
            company="Company B",
            role="Role B",
            status=ApplicationStatus.interviewing,
            applied_date=date(2024, 2, 15)
        ),
        JobApplicationCreate(
            company="Company C",
            role="Role C",
            status=ApplicationStatus.applied,
            applied_date=date(2024, 3, 10)
        ),
        JobApplicationCreate(
            company="Company D",
            role="Role D",
            status=ApplicationStatus.offer,
            applied_date=date(2024, 4, 5)
        ),
        JobApplicationCreate(
            company="Company E",
            role="Role E",
            status=ApplicationStatus.rejected,
            applied_date=date(2024, 5, 20)
        ),
    ]
    created_apps = [services.create_application(app) for app in apps]

    summary = services.get_application_summary()

    assert summary["total"] == 5
    assert summary["by_status"]["applied"] == 2
    assert summary["by_status"]["interviewing"] == 1
    assert summary["by_status"]["offer"] == 1
    assert summary["by_status"]["rejected"] == 1
    assert summary["most_recent"] == created_apps[4]
    assert summary["response_rate"] == 60.0
    assert summary["success_rate"] == 20.0
    assert summary["rejection_rate"] == 20.0


def test_get_application_summary_empty_list():
    summary = services.get_application_summary()

    assert summary["total"] == 0
    assert all(count == 0 for count in summary["by_status"].values())
    assert summary["response_rate"] == 0.0
    assert summary["success_rate"] == 0.0
    assert summary["rejection_rate"] == 0.0
    assert summary["most_recent"] is None
