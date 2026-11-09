
"""Stage 9 integrated SmartCare workflow tests."""

import subprocess
import sys
from pathlib import Path

from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    PatientService,
    PractitionerService,
    AppointmentService,
)


def test_complete_appointment_workflow():
    """UI-01: Verify booking, cancellation, history and slot reuse."""

    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    # Register patient and practitioners.
    patients.register_patient('P1', 'Alice')
    practitioners.register_practitioner('D1', 'Dr Smith', 'GP')
    practitioners.register_practitioner('D2', 'Dr Jones', 'Dentist')

    appointment_time = datetime(2026, 10, 1, 9, 0)

    # Book an appointment with D1.
    first = appointments.book_appointment(
        'A1', 'P1', 'D1', appointment_time
    )

    assert first.status is AppointmentStatus.SCHEDULED

    # D1 cannot have another scheduled appointment at the same time.
    import pytest

    with pytest.raises(ValueError, match='already has a SCHEDULED'):
        appointments.book_appointment(
            'A2', 'P1', 'D1', appointment_time
        )

    # D2 can use the same time.
    second = appointments.book_appointment(
        'A2', 'P1', 'D2', appointment_time
    )

    assert second.status is AppointmentStatus.SCHEDULED

    # Cancel A1 and verify it remains in the store.
    cancelled = appointments.cancel_appointment('A1')

    assert cancelled.status is AppointmentStatus.CANCELLED
    assert store.find_appointment('A1') is first

    # Find the cancelled appointment.
    assert appointments.find_appointment('A1') is first

    # All-status listing retains the cancelled appointment.
    all_d1 = appointments.list_practitioner_appointments('D1')

    assert [item.appointment_id for item in all_d1] == ['A1']
    assert all_d1[0].status is AppointmentStatus.CANCELLED

    # Scheduled-only listing excludes the cancelled appointment.
    scheduled_d1 = appointments.list_practitioner_appointments(
        'D1', AppointmentStatus.SCHEDULED
    )

    assert scheduled_d1 == []

    # The cancelled appointment's time slot can now be reused.
    third = appointments.book_appointment(
        'A3', 'P1', 'D1', appointment_time
    )

    assert third.status is AppointmentStatus.SCHEDULED

    # All-status listing now includes both historical and new records.
    final_d1 = appointments.list_practitioner_appointments('D1')

    assert [item.appointment_id for item in final_d1] == ['A1', 'A3']
    assert final_d1[0].status is AppointmentStatus.CANCELLED
    assert final_d1[1].status is AppointmentStatus.SCHEDULED


def test_interactive_console_workflow_ui01():
    """UI-01: Verify the actual interactive menu using scripted input."""

    project_dir = Path(__file__).resolve().parents[1]

    user_input = (
        '1\n'                  # Register patient
        'P1\n'
        'Alice\n'
        '3\n'                  # Register practitioner D1
        'D1\n'
        'Dr Smith\n'
        'GP\n'
        '3\n'                  # Register practitioner D2
        'D2\n'
        'Dr Jones\n'
        'Dentist\n'
        '5\n'                  # Book A1 with D1
        'A1\n'
        'P1\n'
        'D1\n'
        '2026-10-01 09:00\n'
        '5\n'                  # Attempt conflicting A2 with D1
        'A2\n'
        'P1\n'
        'D1\n'
        '2026-10-01 09:00\n'
        '5\n'                  # Book A2 with D2
        'A2\n'
        'P1\n'
        'D2\n'
        '2026-10-01 09:00\n'
        '6\n'                  # Cancel A1
        'A1\n'
        '7\n'                  # Find A1
        'A1\n'
        '8\n'                  # List all D1 appointments
        'D1\n'
        '\n'
        '8\n'                  # List scheduled D1 appointments
        'D1\n'
        'scheduled\n'
        '5\n'                  # Reuse D1's freed slot
        'A3\n'
        'P1\n'
        'D1\n'
        '2026-10-01 09:00\n'
        '8\n'                  # List all D1 appointments again
        'D1\n'
        '\n'
        '0\n'                  # Exit
    )

    result = subprocess.run(
        [sys.executable, 'main.py', '--interactive'],
        input=user_input,
        capture_output=True,
        text=True,
        cwd=project_dir,
        timeout=10,
    )

    assert result.returncode == 0
    assert 'Patient registered: P1' in result.stdout
    assert 'Appointment booked: A1:' in result.stdout
    assert 'Practitioner already has a SCHEDULED appointment' in result.stdout
    assert 'Appointment booked: A2:' in result.stdout
    assert 'Appointment cancelled: A1:' in result.stdout
    assert 'Appointment found: A1:' in result.stdout
    assert 'No matching appointments found.' in result.stdout
    assert 'Appointment booked: A3:' in result.stdout
    assert 'A1: P1 with D1, 2026-10-01 09:00, cancelled' in result.stdout
    assert 'A3: P1 with D1, 2026-10-01 09:00, scheduled' in result.stdout
    assert 'Exiting SmartCare.' in result.stdout


def test_interactive_console_invalid_input_recovery_ui02():
    """UI-02: Invalid input is handled without crashing or corrupting data."""

    project_dir = Path(__file__).resolve().parents[1]

    user_input = "\n".join([
        "9",                         # Invalid menu choice
        "1", "", "Alice",            # Blank patient ID
        "1", "P1", "Alice",          # Register valid patient
        "1", "P1", "Alice Again",    # Duplicate patient
        "2", "",                     # Blank patient lookup
        "2", "P99",                  # Unknown patient
        "3", "D1", "Dr Smith", "GP", # Register practitioner
        "3", "D1", "Dr Smith", "GP", # Duplicate practitioner
        "4", "D99",                  # Unknown practitioner
        "5", "A1", "PX", "D1", "2026-10-01 09:00",
                                     # Unknown patient during booking
        "5", "A1", "P1", "DX", "2026-10-01 09:00",
                                     # Unknown practitioner during booking
        "5", "A1", "P1", "D1", "01/10/2026 09:00",
                                     # Malformed date
        "5", "A1", "P1", "D1", "2026-02-30 09:00",
                                     # Impossible calendar date
        "5", "A1", "P1", "D1", "2026-10-01 09:00",
                                     # Valid booking; A1 must still be available
        "7", "A99",                  # Unknown appointment
        "6", "A1",                  # First cancellation succeeds
        "6", "A1",                  # Repeated cancellation rejected
        "8", "D1", "invalid",        # Invalid listing status
        "8", "D1", "",               # Valid listing with all statuses
        "0",                         # Exit
    ]) + "\n"

    result = subprocess.run(
        [sys.executable, "main.py", "--interactive"],
        input=user_input,
        capture_output=True,
        text=True,
        cwd=project_dir,
        timeout=10,
    )

    output = result.stdout

    assert result.returncode == 0
    assert "Invalid menu choice" in output
    assert "Patient ID cannot be blank" in output
    assert "Patient ID already exists" in output
    assert "Patient not found" in output
    assert "Practitioner ID already exists" in output
    assert "Practitioner not found" in output
    assert "Use date/time format YYYY-MM-DD HH:MM" in output
    assert "Invalid calendar date/time" in output
    assert "Appointment booked: A1:" in output
    assert "Appointment not found" in output
    assert "Only SCHEDULED appointments may be cancelled" in output
    assert "Status must be scheduled, cancelled, or completed." in output
    assert "A1: P1 with D1, 2026-10-01 09:00, cancelled" in output
    assert "Exiting SmartCare." in output
