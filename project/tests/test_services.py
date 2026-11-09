"""Service tests for Patient, Practitioner, and Appointment workflows."""

import pytest
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.services import (
    PatientService,
    PractitionerService,
    AppointmentService,
)
from smartcare.domain import Appointment, AppointmentStatus


# --- Fixtures for Arrange step (Ensures fresh state for every test) ---

@pytest.fixture
def data_store() -> SmartCareDataStore:
    return SmartCareDataStore()


@pytest.fixture
def patient_service(data_store) -> PatientService:
    return PatientService(data_store)


@pytest.fixture
def practitioner_service(data_store) -> PractitionerService:
    return PractitionerService(data_store)


@pytest.fixture
def appointment_service(data_store) -> AppointmentService:
    return AppointmentService(data_store)


# --- Patient Service Tests (TEST-16, TEST-18) ---

def test_find_registered_patient(patient_service):
    """TEST-18: Service successfully retrieves a registered patient."""
    # Arrange
    patient_service.register_patient('P1', 'Alice')

    # Act
    patient = patient_service.find_patient('P1')

    # Assert
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alice'


def test_find_missing_patient(patient_service):
    """TEST-16: Service raises LookupError for absent patient."""
    # Act & Assert
    with pytest.raises(LookupError, match="Patient not found"):
        patient_service.find_patient('P99')


def test_find_patient_returns_stored_patient(patient_service):
    """Lookup returns the actual stored patient instance."""
    patient_service.register_patient('P1', 'Alex Example')

    result = patient_service.find_patient('P1')

    assert result is patient_service.data_store.find_patient('P1')


def test_find_patient_trims_whitespace(patient_service):
    """Lookup trims whitespace around the patient ID."""
    patient_service.register_patient('P1', 'Alex Example')

    result = patient_service.find_patient('  P1  ')

    assert result.patient_id == 'P1'


def test_find_patient_non_string_id_raises_value_error(patient_service):
    """Lookup rejects non-string patient IDs."""
    with pytest.raises(ValueError, match="Patient ID"):
        patient_service.find_patient(None)


def test_find_patient_is_case_sensitive(patient_service):
    """Lookup does not match patient IDs with different casing."""
    patient_service.register_patient('P1', 'Alex Example')

    with pytest.raises(LookupError):
        patient_service.find_patient('p1')


# --- Practitioner Service Tests (TEST-17) ---

def test_find_registered_practitioner(practitioner_service):
    """Verify Service successfully retrieves a registered practitioner."""
    # Arrange
    practitioner_service.register_practitioner('D1', 'Dr Smith', 'GP')

    # Act
    practitioner = practitioner_service.find_practitioner('D1')

    # Assert
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Dr Smith'
    assert practitioner.specialty == 'GP'


def test_find_missing_practitioner(practitioner_service):
    """TEST-17: Service raises LookupError for absent practitioner."""
    # Act & Assert
    with pytest.raises(LookupError, match="Practitioner not found"):
        practitioner_service.find_practitioner('D99')


# --- Appointment Service Tests (TEST-15) ---

def test_service_cancel_appointment(patient_service, practitioner_service, appointment_service, data_store):
    """TEST-15: Service finds the record, calls domain cancel, returns updated object."""
    # Arrange
    patient_service.register_patient('P1', 'Alice')
    practitioner_service.register_practitioner('D1', 'Dr Smith', 'GP')
    appointment_service.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 9))

    # Act
    cancelled_appt = appointment_service.cancel_appointment('A1')

    # Assert
    assert cancelled_appt.status is AppointmentStatus.CANCELLED
    # Verify it is still retained in the store with the updated status
    assert data_store.find_appointment('A1').status is AppointmentStatus.CANCELLED


def test_service_cancel_missing_appointment(appointment_service):
    """Verify Service raises LookupError when cancelling a non-existent ID."""
    # Act & Assert
    with pytest.raises(LookupError, match="Appointment not found"):
        appointment_service.cancel_appointment('A99')


def test_service_repeated_cancellation_rejected(patient_service, practitioner_service, appointment_service):
    """Verify Service bubbles up the domain ValueError on illegal transitions."""
    # Arrange
    patient_service.register_patient('P1', 'Alice')
    practitioner_service.register_practitioner('D1', 'Dr Smith', 'GP')
    appointment_service.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 9))

    # Cancel it once
    appointment_service.cancel_appointment('A1')

    # Act & Assert: Try to cancel it again via the service
    with pytest.raises(ValueError, match="Only SCHEDULED appointments may be cancelled"):
        appointment_service.cancel_appointment('A1')

# --- Stage 9 Practitioner Appointment Listing Tests (QRY-04) ---


def test_list_practitioner_appointments_includes_all_statuses(
    patient_service,
    practitioner_service,
    appointment_service,
    data_store,
):
    """QRY-04: Omitting status includes scheduled, cancelled and completed."""
    patient = patient_service.register_patient('P1', 'Alice')
    practitioner = practitioner_service.register_practitioner(
        'D1', 'Dr Smith', 'GP'
    )

    # Create a cancelled appointment.
    appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9)
    )
    appointment_service.cancel_appointment('A1')

    # Create a scheduled appointment.
    appointment_service.book_appointment(
        'A2', 'P1', 'D1', datetime(2026, 10, 1, 10)
    )

    # Create a completed appointment.
    completed = Appointment(
        'A3',
        patient,
        practitioner,
        datetime(2026, 10, 1, 11),
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)

    result = appointment_service.list_practitioner_appointments('D1')

    assert [appointment.appointment_id for appointment in result] == [
        'A1', 'A2', 'A3'
    ]
    assert [appointment.status for appointment in result] == [
        AppointmentStatus.CANCELLED,
        AppointmentStatus.SCHEDULED,
        AppointmentStatus.COMPLETED,
    ]


@pytest.mark.parametrize(
    ('status', 'expected_ids'),
    [
        (AppointmentStatus.SCHEDULED, ['A2']),
        (AppointmentStatus.CANCELLED, ['A1']),
        (AppointmentStatus.COMPLETED, ['A3']),
    ],
)
def test_list_practitioner_appointments_filters_by_status(
    patient_service,
    practitioner_service,
    appointment_service,
    data_store,
    status,
    expected_ids,
):
    """QRY-04: A supplied status returns only matching appointments."""
    patient = patient_service.register_patient('P1', 'Alice')
    practitioner = practitioner_service.register_practitioner(
        'D1', 'Dr Smith', 'GP'
    )

    appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9)
    )
    appointment_service.cancel_appointment('A1')

    appointment_service.book_appointment(
        'A2', 'P1', 'D1', datetime(2026, 10, 1, 10)
    )

    data_store.add_appointment(
        Appointment(
            'A3',
            patient,
            practitioner,
            datetime(2026, 10, 1, 11),
            AppointmentStatus.COMPLETED,
        )
    )

    result = appointment_service.list_practitioner_appointments(
        'D1', status
    )

    assert [appointment.appointment_id for appointment in result] == (
        expected_ids
    )


def test_list_practitioner_appointments_only_returns_requested_practitioner(
    patient_service,
    practitioner_service,
    appointment_service,
):
    """QRY-04: Appointments belonging to other practitioners are excluded."""
    patient_service.register_patient('P1', 'Alice')
    practitioner_service.register_practitioner('D1', 'Dr Smith', 'GP')
    practitioner_service.register_practitioner('D2', 'Dr Jones', 'Dentist')

    appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9)
    )
    appointment_service.book_appointment(
        'A2', 'P1', 'D2', datetime(2026, 10, 1, 10)
    )

    result = appointment_service.list_practitioner_appointments('D1')

    assert [appointment.appointment_id for appointment in result] == ['A1']


def test_list_practitioner_appointments_returns_empty_list_when_no_matches(
    practitioner_service,
    appointment_service,
):
    """QRY-04: A known practitioner with no appointments gets an empty list."""
    practitioner_service.register_practitioner('D1', 'Dr Smith', 'GP')

    result = appointment_service.list_practitioner_appointments('D1')

    assert result == []
    assert isinstance(result, list)


def test_list_practitioner_appointments_unknown_practitioner_raises_lookup_error(
    appointment_service,
):
    """QRY-04: An unknown practitioner ID raises LookupError."""
    with pytest.raises(LookupError, match='Practitioner not found'):
        appointment_service.list_practitioner_appointments('D99')


@pytest.mark.parametrize('practitioner_id', ['', '   ', None, 123])
def test_list_practitioner_appointments_invalid_id_raises_value_error(
    appointment_service,
    practitioner_id,
):
    """QRY-04: Blank and non-string practitioner IDs raise ValueError."""
    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments(practitioner_id)


def test_list_practitioner_appointments_invalid_status_raises_value_error(
    practitioner_service,
    appointment_service,
):
    """QRY-04: A status outside AppointmentStatus raises ValueError."""
    practitioner_service.register_practitioner('D1', 'Dr Smith', 'GP')

    with pytest.raises(ValueError, match='Invalid appointment status'):
        appointment_service.list_practitioner_appointments(
            'D1', 'scheduled'
        )