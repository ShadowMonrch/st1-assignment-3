"""Domain tests for Patient, Practitioner, and Appointment."""

import pytest
from datetime import datetime, timezone

from smartcare.domain import (
    Patient,
    Practitioner,
    Appointment,
    AppointmentStatus,
)


# --- Fixtures for Arrange step ---

@pytest.fixture
def valid_patient() -> Patient:
    return Patient('P1', 'Alice')


@pytest.fixture
def valid_practitioner() -> Practitioner:
    return Practitioner('D1', 'Dr Smith', 'GP')


@pytest.fixture
def valid_datetime() -> datetime:
    return datetime(2026, 10, 1, 9, 0)


# --- Reference-Test Intentions ---

def test_blank_patient_id_rejected():
    """TEST-01: Reference intention 1 (Blank patient ID rejected)."""
    # Arrange, Act, Assert
    with pytest.raises(ValueError, match="Patient ID cannot be blank"):
        Patient('   ', 'Alice')


def test_new_appointment_is_scheduled(valid_patient, valid_practitioner, valid_datetime):
    """TEST-02: Reference intention 2 (New appointment starts SCHEDULED)."""
    # Arrange & Act
    appt = Appointment('A1', valid_patient, valid_practitioner, valid_datetime)
    # Assert
    assert appt.status is AppointmentStatus.SCHEDULED


def test_cancellation_changes_status(valid_patient, valid_practitioner, valid_datetime):
    """TEST-03: Reference intention 3 (Cancellation changes status)."""
    # Arrange
    appt = Appointment('A1', valid_patient, valid_practitioner, valid_datetime)
    # Act
    appt.cancel()
    # Assert
    assert appt.status is AppointmentStatus.CANCELLED


def test_repeated_cancellation_rejected(valid_patient, valid_practitioner, valid_datetime):
    """TEST-04: Reference intention 4 (Repeated cancellation is rejected)."""
    # Arrange
    appt = Appointment('A1', valid_patient, valid_practitioner, valid_datetime)
    appt.cancel()
    # Act & Assert
    with pytest.raises(ValueError, match="Only SCHEDULED appointments may be cancelled"):
        appt.cancel()


# --- Additional Required Tests ---

def test_valid_fields_and_trimming():
    """TEST-05: Valid stored field values and trimming."""
    # Act
    p = Patient('  P1  ', '  Alice  ')
    pr = Practitioner('  D1  ', '  Dr Smith  ', '  GP  ')

    # Assert
    assert p.patient_id == 'P1'
    assert p.name == 'Alice'
    assert pr.practitioner_id == 'D1'
    assert pr.name == 'Dr Smith'
    assert pr.specialty == 'GP'


def test_missing_required_fields():
    """TEST-06: Required names and specialty rejected if blank."""
    with pytest.raises(ValueError, match="Patient name cannot be blank"):
        Patient('P1', '  ')
    with pytest.raises(ValueError, match="Practitioner name cannot be blank"):
        Practitioner('D1', ' ', 'GP')
    with pytest.raises(ValueError, match="Specialty cannot be blank"):
        Practitioner('D1', 'Dr Smith', '')


def test_invalid_participant_types(valid_patient, valid_practitioner, valid_datetime):
    """TEST-07: Invalid participant objects rejected."""
    with pytest.raises(ValueError, match="Appointment requires a Patient object"):
        Appointment('A1', 'not a patient', valid_practitioner, valid_datetime)
    with pytest.raises(ValueError, match="Appointment requires a Practitioner object"):
        Appointment('A1', valid_patient, 'not a practitioner', valid_datetime)


def test_invalid_datetime_inputs(valid_patient, valid_practitioner):
    """TEST-08: Invalid date/time formats rejected (seconds, tz, type)."""
    with pytest.raises(ValueError, match="Date/time must be a datetime value"):
        Appointment('A1', valid_patient, valid_practitioner, '2026-10-01')

    with pytest.raises(ValueError, match="Use a local date/time at minute precision"):
        Appointment('A1', valid_patient, valid_practitioner, datetime(2026, 10, 1, 9, 0, 30))

    with pytest.raises(ValueError, match="Use a local date/time at minute precision"):
        Appointment('A1', valid_patient, valid_practitioner, datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc))


def test_invalid_status_input(valid_patient, valid_practitioner, valid_datetime):
    """TEST-09: Invalid status enum rejected."""
    with pytest.raises(ValueError, match="Invalid appointment status"):
        Appointment('A1', valid_patient, valid_practitioner, valid_datetime, status='scheduled')


def test_cancel_completed_appointment(valid_patient, valid_practitioner, valid_datetime):
    """TEST-10: COMPLETED status supplied at construction guards cancellation."""
    # Arrange: Construct directly with COMPLETED status as allowed by prompt
    appt = Appointment('A1', valid_patient, valid_practitioner, valid_datetime, status=AppointmentStatus.COMPLETED)
    # Act & Assert
    with pytest.raises(ValueError, match="Only SCHEDULED appointments may be cancelled"):
        appt.cancel()