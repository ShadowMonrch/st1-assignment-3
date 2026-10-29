
from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def setup_appointment():
    """Create a registered patient, practitioner and appointment."""
    store = SmartCareDataStore()

    patient = PatientService(store).register_patient(
        "P1", "Alex Example"
    )
    practitioner = PractitionerService(store).register_practitioner(
        "D1", "Taylor Example", "General"
    )

    service = AppointmentService(store)
    appointment = service.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 29, 9, 0),
    )

    return store, service, appointment


def test_cancel_appointment_changes_status():
    store, service, appointment = setup_appointment()

    result = service.cancel_appointment("A1")

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED


def test_cancel_appointment_retains_history():
    store, service, appointment = setup_appointment()

    service.cancel_appointment("A1")

    assert store.find_appointment("A1") is appointment
    assert store.list_appointments() == [appointment]


def test_cancel_unknown_appointment_raises_lookup_error():
    _, service, _ = setup_appointment()

    with pytest.raises(LookupError):
        service.cancel_appointment("A999")


def test_cancel_appointment_twice_raises_value_error():
    _, service, appointment = setup_appointment()

    service.cancel_appointment("A1")

    with pytest.raises(ValueError):
        service.cancel_appointment("A1")

    assert appointment.status is AppointmentStatus.CANCELLED


def test_cancel_blank_appointment_id_raises_value_error():
    _, service, appointment = setup_appointment()

    with pytest.raises(ValueError):
        service.cancel_appointment(" ")

    assert appointment.status is AppointmentStatus.SCHEDULED
