import pytest
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    PatientService,
    PractitionerService,
    AppointmentService,
)


def test_f8_01_practitioner_conflict():
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patients.register_patient("P1", "Alice")
    patients.register_patient("P2", "Bob")
    practitioners.register_practitioner("D1", "Dr Smith", "GP")
    practitioners.register_practitioner("D2", "Dr Jones", "GP")

    when = datetime(2026, 10, 1, 9)

    first = appointments.book_appointment("A1", "P1", "D1", when)

    # The same practitioner cannot be double-booked.
    with pytest.raises(ValueError):
        appointments.book_appointment("A2", "P2", "D1", when)

    # A rejected booking must not change stored appointments.
    assert store.find_appointment("A2") is None
    assert store.list_appointments() == [first]

    # A different practitioner can be booked at the same time.
    second = appointments.book_appointment("A3", "P2", "D2", when)
    assert store.find_appointment("A3") is second


def test_f8_02_cancelled_appointment_retained():
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patients.register_patient("P1", "Alice")
    practitioners.register_practitioner("D1", "Dr Smith", "GP")

    original = appointments.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9)
    )

    cancelled = appointments.cancel_appointment("A1")

    assert cancelled is original
    assert original.status is AppointmentStatus.CANCELLED
    assert original in store.list_appointments()
    # The original appointment must remain stored and accessible.
    assert store.find_appointment("A1") is original
    assert appointments.find_appointment("A1") is original
    assert original in store.list_appointments()

    # Repeated cancellation must be rejected.
    with pytest.raises(ValueError):
        appointments.cancel_appointment("A1")

    assert original.status is AppointmentStatus.CANCELLED
