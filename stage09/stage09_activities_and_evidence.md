# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification
| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Required session/domain state | Needed to identify registered patients and associate them with appointments during the session. |
| Appointment history | Required session/domain state | Needed to retrieve previous appointments, including cancelled appointments, during the session. |
| Temporary menu choice | Transient interaction state | Only needed while processing the user's current menu selection. It does not need to be retained. |
| Practitioner specialty | Required session/domain state | Needed to retain practitioner details and provide accurate practitioner information during the session. |
| Debug print output | Transient debug state | Used temporarily by developers to troubleshoot the application. It is not part of the application's domain data. |
| Appointment status | Required session/domain state | Needed to distinguish scheduled and cancelled appointments and enforce valid appointment operations. |

What is intentionally lost on exit?

<!-- response -->
All in-memory session data is intentionally lost when the program exits, including registered patient details, practitioner details, appointment records and appointment statuses. Temporary menu selections and debugging output are also not retained. The application uses in-memory storage rather than permanent database storage, so a new session starts with empty collections.

### A2 Interface and domain data plan

## A2 – Plan Before AI

No database tables are required. The design uses the existing SmartCare domain classes, services and data store.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| `appointment_sort_key` | `appointment: Appointment` | `tuple[datetime, str]` | Returns a sorting key using appointment date/time first and appointment ID second. Does not modify the appointment. | Uses `Appointment.date_time` and `Appointment.appointment_id`. |
| `select_appointments` | `appointments: list[Appointment]`, `practitioner_id: str`, `status: AppointmentStatus \| None = None` | `list[Appointment]` | Filters appointments by practitioner ID and optional status. Returns a new list sorted by date/time and appointment ID. Does not modify the original list or appointment objects. | Uses `Appointment.practitioner.practitioner_id`, `Appointment.status`, `Appointment.date_time` and `Appointment.appointment_id`. |
| Service listing | `practitioner_id: str`, `status: AppointmentStatus \| None = None` | `list[Appointment]` | Checks that the practitioner exists, retrieves appointments from the data store and delegates filtering and sorting to `select_appointments`. Raises `LookupError` for an unknown practitioner and `ValueError` for invalid input. | Uses the existing `PractitionerService`, `AppointmentService` and shared `SmartCareDataStore`. |
| Console | User input collected during menu execution | `None` | Displays the menu, accepts user choices, calls the appropriate services, displays results and handles expected errors. Continues until the user chooses to exit. | Uses existing patient, practitioner and appointment services, `parse_date_time()` and `format_appointment()`. |

### Domain sources and existing constraints

Patient identity comes from the existing `Patient` object, using its `patient_id` and `name` attributes. Practitioner identity and details come from the existing `Practitioner` object, using its `practitioner_id`, `name` and `specialty` attributes.

Appointment information comes from the existing `Appointment` object. It contains an `appointment_id`, the actual registered `Patient` and `Practitioner` objects, a `date_time` value and an `AppointmentStatus` value.

The appointment must reference the actual participant objects registered in the shared data store. Creating replacement objects with matching IDs is not sufficient.

Existing constraints must be preserved:
- IDs and names must be valid, non-blank strings.
- IDs are trimmed and case-sensitive.
- Appointment date/time must follow the existing datetime validation.
- Appointment status must use the existing `AppointmentStatus` enum.
- Duplicate appointment IDs must be rejected.
- Appointments must reference registered patients and practitioners.
- A practitioner cannot have two scheduled appointments at the same date and time.
- Cancelled appointments remain stored so their history can be retrieved.
- Rejected operations must not modify existing stored data.

---

## Record B – Requirements, Operations and Expected Behaviour

| Requirement | Operation / responsibility | Expected behaviour | Test / evidence |
|---|---|---|---|
| QRY-01 – Appointment sorting key | `appointment_sort_key()` | Returns a tuple containing appointment date/time followed by appointment ID. | `test_appointment_sort_key_returns_datetime_and_id` |
| QRY-02 – Practitioner filtering | `select_appointments()` | Returns only appointments belonging to the requested practitioner. | `test_select_appointments_filters_by_practitioner` |
| QRY-03 – Status filtering | `select_appointments()` | When a status is supplied, returns only appointments with that status. When no status is supplied, includes all statuses. | `test_select_appointments_filters_by_status` |
| QRY-04 – Appointment ordering | `select_appointments()` | Returns appointments sorted by date/time, using appointment ID to break ties. | `test_select_appointments_returns_sorted_appointments` |
| QRY-05 – Original collection preservation | `select_appointments()` | Returns a new list without modifying the original appointment list or its objects. | `test_select_appointments_does_not_modify_original_list` |
| FP-01 – Pure function behaviour | `appointment_sort_key()` and `select_appointments()` | Query functions depend only on their inputs and do not perform input/output or modify stored data. | `test_query_functions_are_repeatable_and_do_not_modify_data` |
| FR-01 – Patient registration | `PatientService.register_patient()` | Registers a valid patient and rejects invalid or duplicate patient IDs. | `test_register_patient` |
| FR-02 – Patient lookup | `PatientService.find_patient()` | Returns the registered patient. Raises `LookupError` for an unknown ID and `ValueError` for invalid input. | `test_find_patient` |
| FR-03 – Practitioner registration | `PractitionerService.register_practitioner()` | Registers a valid practitioner with their name and specialty. Rejects invalid or duplicate details. | `test_register_practitioner` |
| FR-04 – Practitioner lookup | `PractitionerService.find_practitioner()` | Returns the registered practitioner. Raises `LookupError` for an unknown ID and `ValueError` for invalid input. | `test_find_practitioner` |
| FR-05 – Appointment booking | `AppointmentService.book_appointment()` | Books an appointment using the actual registered patient and practitioner objects. Rejects duplicate IDs, invalid participants and scheduling conflicts. | `test_book_appointment` |
| FR-06 – Appointment lookup | `AppointmentService.find_appointment()` | Returns the stored appointment, including cancelled appointments. Raises `LookupError` for an unknown ID and `ValueError` for invalid input. | `test_find_appointment_includes_cancelled` |
| FR-07 – Appointment cancellation | `AppointmentService.cancel_appointment()` | Changes the appointment status to cancelled without deleting its history. Rejects repeated cancellation. | `test_cancel_appointment_and_retain_history` |
| FR-08 – Practitioner appointment listing | `AppointmentService.list_practitioner_appointments()` | Returns appointments belonging to the requested practitioner, in the correct order, with optional status filtering. | `test_list_practitioner_appointments` |
| FR-09 – Appointment integrity | Domain classes, services and data store | Ensures appointments use registered participant objects, unique IDs and valid scheduling rules. Rejected operations leave stored data unchanged. | `test_appointment_integrity_and_rejected_operations` |
| UI-01 – Interactive menu | `run_menu()` | Displays available actions and allows users to register, find, book, cancel and list appointments. | `test_menu_full_workflow` |
| UI-02 – Invalid menu input | `run_menu()` | Displays appropriate error messages for invalid choices or inputs and allows the user to continue using the application. | `test_menu_recovers_from_invalid_input` |
| UI-03 – Exit behaviour | `run_menu()` | Allows the user to exit the application cleanly. | `test_menu_exits_cleanly` |

### Record B – Design Decisions

| Topic | Decision and reasoning |
|---|---|
| Empty results | A known practitioner with no matching appointments returns an empty list. This is a valid result, not an error. |
| Unknown practitioner | An unknown practitioner ID raises `LookupError`. The system must not silently create a practitioner. |
| Invalid input | Blank IDs, invalid types and invalid status values are rejected using the existing validation rules. |
| Enum conversion | Console input is received as text. Valid status input must be converted into the corresponding `AppointmentStatus` enum member before calling the service. Invalid status choices are rejected. |
| Actual object identity | Appointments must reference the same registered `Patient` and `Practitioner` objects held in the shared data store. Matching IDs alone are insufficient. |
| Error handling | Services and domain objects handle validation and raise appropriate exceptions. The console catches expected errors, displays a message and allows the user to continue. |
| Unchanged state | If an operation fails, existing patients, practitioners, appointments and appointment statuses must remain unchanged. |
| Separation of responsibilities | Query functions perform filtering and sorting, services coordinate business operations and data access, and the console handles user interaction. |

### What Is Intentionally Lost When the Program Exits?

All in-memory session data is intentionally lost when the program exits. This includes registered patients, practitioner details, appointment records and appointment statuses. Temporary menu choices and debugging output are also not retained.

The application uses in-memory storage rather than permanent database storage, so a new session starts with empty collections.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | The `Appointment` domain object is handling user interaction by calling `input()`. This mixes domain logic with the console interface and makes the method difficult to test independently. | The console should ask the user for confirmation and pass the decision to the appropriate service or domain operation. `Appointment.cancel()` should only handle the appointment's cancellation rules and update its status. |
| Service prints/reads the menu | The service is handling presentation and user interaction instead of focusing on business operations. This tightly couples the service to the console and makes it harder to reuse or test. | The console should display the menu, read the user's command and call the appropriate service method. The service should perform the requested operation, validate business rules and return a result or raise an appropriate exception. |
| Query sorts its source in place | Calling `appointments.sort()` changes the original list supplied to the query function. This introduces an unwanted side effect and can affect other parts of the application that use the same list. | The query function should use `sorted()` to create and return a new sorted list. This preserves the original collection and supports predictable, repeatable query behaviour. |
| Store prints Appointment saved | The store is handling presentation by printing a message instead of providing a useful result to the service. Printing does not allow the calling code to inspect or use the saved appointment. | The store should save the appointment and return the stored `Appointment` object. The service can then use the returned object, and the console can display an appropriate success message. Returning the object also allows the caller to verify which appointment was saved and preserves separation between storage and presentation. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check:

| Sorting operation | Changes source order? | Return value | Result identity |
|---|---|---|---|
| `appointments.sort(key=appointment_sort_key)` | Yes. The original `appointments` list is sorted in place. | `None` | No new list is created. The original list is modified. |
| `result = sorted(appointments, key=appointment_sort_key)` | No. The original `appointments` list keeps its original order. | A new sorted list. | `result is appointments` evaluates to `False`. |

A meaningful mutation check is to save a copy of the original list before sorting and compare it afterwards. Checking only the length is insufficient because sorting can change the order without changing the number of elements.

Example:


original_order = appointments.copy()

result = sorted(appointments, key=appointment_sort_key)

assert appointments == original_order
assert result is not appointments
assert result == sorted(original_order, key=appointment_sort_key)

### A5 Exit question

Cancellation changes an appointment's status rather than deleting the appointment because SmartCare must retain appointment history. Keeping the original appointment allows the system to identify that the appointment existed, who it involved, when it was scheduled and whether it was cancelled. Deleting it would permanently remove this information and make it impossible to retrieve its history during the session.

The following checks demonstrate that cancellation retains appointment history:

1. **Same-session lookup:** After cancelling an appointment, retrieve it using its appointment ID. The lookup should return the same appointment object, with its status changed to `CANCELLED`, rather than returning `None` or raising `LookupError`.

2. **All-status listing:** List the practitioner's appointments without specifying a status filter. The cancelled appointment should still appear in the returned list, alongside scheduled appointments. This demonstrates that cancellation does not remove the appointment from storage.

3. **SCHEDULED-only exclusion:** List the practitioner's appointments with the `SCHEDULED` status filter. The cancelled appointment should not appear because its status is now `CANCELLED`. This ensures that cancelled appointments remain available as historical records without being treated as upcoming scheduled appointments.

These checks demonstrate the difference between retaining an appointment and including it in a particular filtered result. Cancellation updates the appointment's status, while status filtering determines which appointments are returned.

## B. Human design and contracts

The query functions will be implemented as pure functions using the supplied typed contracts in `project/smartcare/queries.py`.

The design separates query processing from service validation and console interaction. Query functions operate only on the supplied appointment objects and filter values. They do not access the global data store, perform input/output or modify the original collection or appointment objects.

### Interface and integrity decisions

- `appointment_sort_key(appointment)` accepts an `Appointment` object and returns a tuple containing its `date_time` and `appointment_id`.
- `select_appointments(appointments, practitioner_id, status=None)` accepts a list of appointments, a practitioner ID and an optional `AppointmentStatus`.
- The default `status=None` includes appointments with every status, including `CANCELLED` and `COMPLETED`.
- When an explicit status is provided, only appointments matching that enum value are returned.
- Results are returned as a new list sorted in ascending order by `(date_time, appointment_id)`.
- The named `appointment_sort_key` function must be used for sorting.
- The returned list may contain references to the original appointment objects. The objects themselves must not be modified.
- Practitioner registration is not checked by the pure query helper. That responsibility belongs to the service listing operation.
- The original source collection must retain its original order, including when the input is empty, already sorted or unsorted.

### Requirements, operations and expected behaviour

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 – Practitioner filtering | Appointment list and requested practitioner ID, including appointments belonging to another practitioner as a control. | `select_appointments()` – pure query function. | Returns only appointments belonging to the requested practitioner. Appointments belonging to other practitioners are excluded. | QRY-01: Verify matching practitioner appointments are returned and the other practitioner's appointment is excluded. |
| QRY-02 – Status filtering | Appointment list containing `SCHEDULED`, `CANCELLED` and `COMPLETED` appointments. | `select_appointments()` – pure query function. | With `status=None`, returns all statuses. With an explicit enum status, returns only matching appointments. A status with no matches returns an empty list. | QRY-02: Test the default status, each explicit enum status and a no-match status. |
| QRY-03 – Sorting and source preservation | Appointments with different date/times and appointments sharing a date/time but having different appointment IDs. | `appointment_sort_key()` and `select_appointments()` – pure query functions. | Results are sorted ascending by date/time and then appointment ID. The original source order and appointment fields remain unchanged. | QRY-03: Snapshot source order and relevant fields, query the appointments and compare the source before and after. |
| QRY-04 – Sorting key contract | Individual `Appointment` objects containing date/time and appointment ID values. | `appointment_sort_key()` – pure query function. | Returns the correct `(date_time, appointment_id)` tuple for each appointment. | QRY-04: Directly test the named sorting key and verify its returned values. |
| FP-01 – Purity and repeatability | The same valid appointment list and filter values supplied repeatedly. | `select_appointments()` – pure query function. | Repeated calls with unchanged inputs produce equivalent results without hidden state, input/output or side effects. | FP-01: Repeat the query and compare results. Inspect the implementation for global state, input/output and mutations. |
| FP-02 – New list identity | Empty, already-sorted and unsorted appointment lists. | `select_appointments()` – pure query function. | Returns a distinct list for every input case. The returned list can contain the same appointment object references, but the source list and appointment objects remain unchanged. | FP-02: Check that the result is not the source list using `is not`, compare source order and verify appointment fields remain unchanged. |
| FP-03 – Named key usage | Appointment objects with different date/times and equal-time appointments with different IDs. | `appointment_sort_key()` and `select_appointments()` – pure query functions. | The named key returns the expected sorting tuple and is used by the selection function to sort appointments. | FP-03: Test the key directly and inspect or verify that the selection function uses it. |
| UI-01 – Menu interaction | User's menu choice and relevant registration, booking or listing information. | Console/menu – presentation component. | Displays the available operations, accepts a menu choice and calls the appropriate service operation. | UI-01: Test a valid menu choice and verify the expected operation is performed. |
| UI-02 – Invalid menu input | Invalid menu choices and invalid user-entered values. | Console/menu – presentation component. | Displays an appropriate error and allows the user to continue rather than terminating unexpectedly. | UI-02: Test invalid input and verify the menu continues. |
| FR-01 – Patient registration | Patient ID and patient name. | Patient service. | Registers a valid patient and rejects invalid or duplicate patient information. | Verify successful registration and rejection of invalid or duplicate details. |
| FR-02 – Patient lookup | Patient ID. | Patient service. | Returns the registered patient. An unknown patient raises `LookupError`; invalid input raises `ValueError`. | Verify successful lookup, unknown ID and invalid ID. |
| FR-03 – Practitioner registration | Practitioner ID, name and specialty. | Practitioner service. | Registers a valid practitioner and rejects invalid or duplicate practitioner information. | Verify successful registration and rejection of invalid or duplicate details. |
| FR-04 – Practitioner lookup | Practitioner ID. | Practitioner service. | Returns the registered practitioner. An unknown practitioner raises `LookupError`; invalid input raises `ValueError`. | Verify successful lookup, unknown ID and invalid ID. |
| FR-05 – Appointment booking | Appointment ID, patient ID, practitioner ID and date/time. | Appointment service and data store. | Creates an appointment using the actual registered patient and practitioner objects. Rejects invalid participants, duplicate IDs and scheduling conflicts. | Verify successful booking, participant identity and rejected booking cases. |
| FR-06 – Appointment lookup | Appointment ID. | Appointment service and data store. | Returns the stored appointment, including cancelled appointments. Unknown IDs and invalid IDs are handled using the existing exception contracts. | Verify successful lookup and retrieval of cancelled appointment history. |
| FR-07 – Appointment cancellation | Appointment ID. | Appointment service and appointment domain object. | Changes the appointment status to `CANCELLED` without deleting its stored record. Repeated cancellation is rejected. | Verify status change, retained lookup and rejection of repeated cancellation. |
| FR-08 – Appointment listing | Practitioner ID and optional appointment status. | Appointment service and pure query function. | Checks that the practitioner exists, then returns the practitioner's appointments using the query function. A known practitioner with no matching appointments receives an empty list. | Verify practitioner filtering, status filtering, sorting and unknown practitioner handling. |
| FR-09 – Appointment integrity | Registered patient and practitioner objects, appointment ID, date/time and status. | Domain objects, appointment service and data store. | Preserves valid participant references, unique appointment IDs and scheduling rules. Rejected operations do not modify stored state. | Verify participant identity, duplicate rejection, conflict rejection and unchanged state after failure. |

### Explanation of important design decisions

**Empty versus unknown versus invalid**

An empty result is not automatically an error. If a practitioner exists but has no appointments matching the requested status, the query returns an empty list. An unknown practitioner is different: the service must raise `LookupError` because the requested practitioner is not registered. Invalid values, such as a blank practitioner ID or an invalid status type, must be rejected using the existing validation rules.

**Enum conversion**

The console receives user input as text. If the user selects a status, the console or appropriate service boundary must convert that input into the matching `AppointmentStatus` enum member before passing it to the query function. Invalid status choices must be handled without crashing the application. The query function receives the enum value rather than performing interactive input.

**Actual object identity**

An appointment must reference the actual registered `Patient` and `Practitioner` objects held in the shared data store. Creating different objects with matching IDs is not sufficient. This maintains the relationship between appointments and their registered participants.

**Error handling**

Domain objects and services are responsible for enforcing their existing validation and business rules. They should raise appropriate exceptions when an operation is invalid. The console catches expected exceptions, displays a useful message and allows the user to continue using the application.

**Unchanged state on rejection**

If an appointment booking, cancellation or other operation is rejected, existing stored data must remain unchanged. This includes appointment records, participant references and appointment statuses. Tests should inspect the relevant state before and after rejected operations to confirm that no partial changes occurred.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| QRY-01 | `project/smartcare/queries.py`, `project/tests/test_queries.py` | Verify that only appointments belonging to the requested practitioner are returned, with another practitioner's appointment used as a control. | Passed | `test_queries.py` |
| QRY-02 | `project/smartcare/queries.py`, `project/tests/test_queries.py` | Verify that `status=None` includes all statuses, each explicit `AppointmentStatus` returns matching appointments, and a status with no matches returns an empty list. | Passed | `test_queries.py` |
| QRY-03 | `project/smartcare/queries.py`, `project/tests/test_queries.py` | Verify ascending date/time ordering, appointment ID tie-breaking for equal times, and that the original list and appointment fields remain unchanged. | Passed | `test_queries.py` |
| FP-01 | `project/smartcare/queries.py`, `project/tests/test_queries.py` | Repeat queries with unchanged inputs and verify equivalent results. Inspect the implementation for hidden state, input/output and side effects. | Passed | `test_queries.py` and code inspection |
| FP-02 | `project/smartcare/queries.py`, `project/tests/test_queries.py` | Verify that empty, already-sorted and unsorted inputs produce a distinct result list while preserving the original list and contained appointment objects. | Passed | `test_queries.py` |
| FP-03 | `project/smartcare/queries.py`, `project/tests/test_queries.py` | Directly test `appointment_sort_key()` and verify that `select_appointments()` uses the named key for sorting. | Passed | `test_queries.py` |

### Overall verification

**Command:** `python -m pytest -q`

**Working directory:** `project/`

**Actual result:** 37 passed.

The complete existing test suite and the new Stage 9 query tests passed together. Passing tests provide evidence of correct behaviour, but do not independently prove purity. Code inspection is also required to confirm that the query functions do not access hidden state, perform input/output or modify their inputs.

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- response -->
What the tests do and do not establish: <!-- response -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
