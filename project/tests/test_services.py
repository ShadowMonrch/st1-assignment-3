"""Service tests for Patient, Practitioner, and Appointment workflows."""

import pytest
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.services import (
    PatientService,
    PractitionerService,
    AppointmentService,
)
from smartcare.domain import AppointmentStatus


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