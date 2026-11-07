"""Stage 9 Step 5: QRY-01–03 and FP-01–03."""
from datetime import datetime

import pytest

from smartcare.domain import Appointment, AppointmentStatus, Patient, Practitioner
from smartcare.queries import appointment_sort_key, select_appointments


def fixtures():
    patient = Patient('P1', 'Test Patient')
    d1 = Practitioner('D1', 'Doctor One', 'General')
    d2 = Practitioner('D2', 'Doctor Two', 'General')
    t1 = datetime(2026, 10, 1, 9, 0)
    t2 = datetime(2026, 10, 1, 10, 0)
    return [
        Appointment('A3', patient, d1, t1, AppointmentStatus.CANCELLED),
        Appointment('A9', patient, d2, t1, AppointmentStatus.SCHEDULED),
        Appointment('A2', patient, d1, t2, AppointmentStatus.SCHEDULED),
        Appointment('A1', patient, d1, t1, AppointmentStatus.COMPLETED),
        Appointment('A4', patient, d1, t1, AppointmentStatus.CANCELLED),
    ]


def ids(items):
    return [a.appointment_id for a in items]


def snapshot(items):
    return [
        (id(a), a.appointment_id, a.patient, a.practitioner, a.date_time, a.status)
        for a in items
    ]


def test_qry01_practitioner_isolation():
    source = fixtures()
    assert ids(select_appointments(source, 'D1')) == ['A1', 'A3', 'A4', 'A2']
    assert ids(select_appointments(source, 'D2')) == ['A9']


def test_qry02_default_all_and_explicit_statuses():
    source = fixtures()
    assert ids(select_appointments(source, 'D1')) == ['A1', 'A3', 'A4', 'A2']
    assert ids(select_appointments(source, 'D1', AppointmentStatus.SCHEDULED)) == ['A2']
    assert ids(select_appointments(source, 'D1', AppointmentStatus.CANCELLED)) == ['A3', 'A4']
    assert ids(select_appointments(source, 'D1', AppointmentStatus.COMPLETED)) == ['A1']
    assert select_appointments(source, 'D2', AppointmentStatus.COMPLETED) == []


def test_qry03_order_and_no_mutation():
    source = fixtures()
    before = snapshot(source)
    result = select_appointments(source, 'D1')
    assert ids(result) == ['A1', 'A3', 'A4', 'A2']
    assert snapshot(source) == before
    assert all(any(item is original for original in source) for item in result)


def test_fp01_repeatability_and_no_side_effects(capsys):
    source = fixtures()
    before = snapshot(source)
    first = select_appointments(source, 'D1')
    second = select_appointments(source, 'D1')
    assert ids(first) == ids(second)
    assert snapshot(source) == before
    assert capsys.readouterr() == ('', '')


@pytest.mark.parametrize('kind', ['empty', 'sorted', 'unsorted'])
def test_fp02_fresh_list_for_all_source_orders(kind):
    source = fixtures()
    if kind == 'empty':
        source = []
    elif kind == 'sorted':
        source = sorted(source, key=appointment_sort_key)
    before = snapshot(source)
    result = select_appointments(source, 'D1')
    assert result is not source
    assert snapshot(source) == before
    assert all(any(item is original for original in source) for item in result)


def test_fp03_named_key_directly():
    source = fixtures()
    appointment = source[0]
    assert appointment_sort_key(appointment) == (datetime(2026, 10, 1, 9, 0), 'A3')
    assert ids(select_appointments(source, 'D1')) == ['A1', 'A3', 'A4', 'A2']
