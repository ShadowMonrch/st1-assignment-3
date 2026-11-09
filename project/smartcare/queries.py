"""Stage 9 contracts for pure collection processing."""
from datetime import datetime
from smartcare.domain import Appointment, AppointmentStatus


def appointment_sort_key(appointment: Appointment) -> tuple[datetime, str]:
    """Return the appointment date/time and ID without side effects."""
    return appointment.date_time, appointment.appointment_id


def select_appointments(
    appointments: list[Appointment],
    practitioner_id: str,
    status: AppointmentStatus | None = None,
) -> list[Appointment]:
    """Select a practitioner's appointments in ascending order without mutation."""
    matching = [
        appointment
        for appointment in appointments
        if appointment.practitioner.practitioner_id == practitioner_id
        and (status is None or appointment.status is status)
    ]
    return sorted(matching, key=appointment_sort_key)
