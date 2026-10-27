
import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService


def setup_patient_service():
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    patient = patient_service.register_patient("P1", "Alex Example")
    return data_store, patient_service, patient


def test_find_patient_returns_stored_patient():
    _, patient_service, patient = setup_patient_service()

    result = patient_service.find_patient("P1")

    assert result is patient


def test_find_patient_trims_whitespace():
    _, patient_service, patient = setup_patient_service()

    result = patient_service.find_patient("  P1  ")

    assert result is patient


def test_find_patient_missing_id_raises_lookup_error():
    _, patient_service, _ = setup_patient_service()

    with pytest.raises(LookupError):
        patient_service.find_patient("P2")


def test_find_patient_blank_id_raises_value_error():
    _, patient_service, _ = setup_patient_service()

    with pytest.raises(ValueError):
        patient_service.find_patient("   ")


def test_find_patient_is_case_sensitive():
    _, patient_service, _ = setup_patient_service()

    with pytest.raises(LookupError):
        patient_service.find_patient("p1")
