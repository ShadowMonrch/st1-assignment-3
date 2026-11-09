# SmartCare — Undergraduate Release

## Overview

SmartCare is a Python-based teaching application for managing
synthetic patient, practitioner and appointment records.

The application supports patient and practitioner registration
and lookup, appointment booking, cancellation, appointment lookup,
and practitioner appointment listings.

This release covers the Undergraduate (UG) pathway.

## Requirements

- Python 3.13
- pytest 8.3.5 for development and testing

The application uses only the Python standard library at runtime.

## Setup

Open a terminal in the project directory.

Install the development dependency:

    python -m pip install -r requirements-dev.txt

## Running the application

Run the standard demonstration:

    python main.py

Start the interactive menu:

    python main.py --interactive

The interactive menu supports:

1. Register a patient
2. Find a patient
3. Register a practitioner
4. Find a practitioner
5. Book an appointment
6. Cancel an appointment
7. Find an appointment
8. List a practitioner's appointments
0. Exit

Appointment date and time input must use:

    YYYY-MM-DD HH:MM

## Running the tests

From the project directory, run the complete test suite:

    python -m pytest -v

The release candidate was tested using Python 3.13.14
and pytest 8.3.5. The recorded full-suite result was
52 passing tests.

## Main project structure

- main.py — application entry point.
- smartcare/domain.py — patient, practitioner and appointment
  entities, validation and appointment status transitions.
- smartcare/data_store.py — in-memory storage and record access.
- smartcare/services.py — registration, lookup, booking,
  cancellation and practitioner appointment workflows.
- smartcare/queries.py — appointment filtering and sorting.
- smartcare/console.py — demonstration and interactive menu.
- tests/ — automated tests for domain rules, services,
  queries and interactive workflows.

## Important behaviour and limitations

- Data is stored in memory and exists only for the current session.
- Records are lost when the application exits.
- Only synthetic information should be used.
- Appointment cancellation changes the appointment status
  to cancelled; it does not delete the record.
- A practitioner cannot have two scheduled appointments
  at the same date and time.
- Practitioner appointment listings can filter by status
  and are sorted chronologically.
- The application does not implement persistent storage,
  deployment, or production healthcare functionality.
- No clinical or security certification is claimed.

## UG release scope

This release implements the Undergraduate pathway requirements.
Postgraduate-only functionality is outside this release's scope.

The application is an educational software project and must not
be used to manage real patient information or clinical appointments.
