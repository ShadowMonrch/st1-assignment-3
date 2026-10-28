# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

# Stage 7: Activity 1 - Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| **FR-01 Register patient** | Call `PatientService.register_patient("P1", "Alex Example")` with a unique ID and valid name. | Attempt to register a patient with a blank name (e.g., `"   "`), or attempt to register a duplicate ID (e.g., `"P1"` twice). | The valid patient is added to the `SmartCareDataStore`. The invalid attempts raise a `ValueError` (due to `required_text` or duplicate ID check in `add_patient`). |
| **FR-05 Prevent practitioner conflict** | Book Practitioner "DR1" at `2026-10-01 09:00`, then successfully book "DR1" at `2026-10-01 10:00`. | Book "DR1" at `09:00`, then attempt to book "DR1" at `09:00` on the same date. | The second booking at the exact same time raises a `ValueError`. The check relies on `SmartCareDataStore.has_practitioner_conflict()` returning `True`. |
| **FR-06 Cancel appointment** | Call `AppointmentService.cancel_appointment("A1")` on an appointment with a `SCHEDULED` status. | Attempt to cancel an appointment that is already `CANCELLED` or `COMPLETED`. | The status successfully changes to `AppointmentStatus.CANCELLED`. The invalid attempt triggers the guard in `Appointment.cancel()` and raises a `ValueError` without changing the state. |
| **FR-07 Retain cancelled history** | Cancel appointment "A1", then call `AppointmentService.find_appointment("A1")`. | Call `AppointmentService.find_appointment("A99")` (an ID that does not exist). | The cancelled appointment remains in the `SmartCareDataStore._appointments` dictionary and is returned by `find_appointment` with its status correctly showing as `CANCELLED`. The missing ID raises a `LookupError`. |
### Activity 2 Strong or weak assertion
# Stage 7: Activity 2 - Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

**`assert True`**
Judgement: **Weak/unclear**  
Why: It asserts absolutely nothing and will always pass. It provides zero coverage and catches no bugs, regardless of whether the `SmartCareDataStore` or domain rules are broken.
*Behaviour and limits:* Tests no behaviour. Limit: A completely useless test that creates a false sense of security.

**`assert appointment is not None`**
Judgement: **Weak/unclear**  
Why: It only proves that `find_appointment()` returned an object. It doesn't verify if it's the *correct* appointment, nor does it check if the patient or practitioner references inside it are valid.
*Behaviour and limits:* Tests basic object retrieval. Limit: The data store could return a completely wrong appointment, and this test would still pass.

**`assert appointment.status == AppointmentStatus.CANCELLED`**
Judgement: **Strong**  
Why: It explicitly verifies the business rule. It checks that the state transition logic in `Appointment.cancel()` actually executed and resulted in the exact expected Enum state.
*Behaviour and limits:* Tests the specific state transition of an appointment. Limit: It doesn't verify that the appointment remains retrievable in the `SmartCareDataStore` after cancellation, only that the object's status mutated.

**`assert len(results) > 0`**
Judgement: **Weak/unclear**  
Why: It only proves that a list has at least one item. If a query like `list_appointments()` or a future `select_appointments()` returns 100 wrong records or unregistered objects, this test still passes.
*Behaviour and limits:* Tests that a collection is not empty. Limit: It cannot detect false positives, irrelevant data, or missing records.

**`assert data_store.find_appointment('A1') is appointment`**
Judgement: **Strong**  
Why: It checks identity (`is`) rather than just equality. It proves that the `SmartCareDataStore` correctly stored and retrieved the *exact same object instance* in memory, ensuring no copying or substitution occurred.
*Behaviour and limits:* Tests the data store's ability to map an ID to a specific in-memory instance. Limit: This works perfectly for session-only in-memory storage, but would need to change to an equality (`==`) check if a future SQLite implementation serializes and deserializes the data.
### Activity 3 Boundary thinking
# Stage 7: Activity 3 - Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract:


| Input / State | Expected Result | Supporting Contract (Evidence) |
|---|---|---|
| **Blank identifiers**<br>e.g., `PatientService.register_patient("", "Alex")` or `AppointmentService.find_appointment("")` | The system raises a `ValueError` indicating the ID cannot be blank. The object is not created, and no lookup is performed. | **Contract:** `required_text()` in `domain.py`.<br>*Code:* `if not isinstance(value, str) or not value.strip(): raise ValueError(...)` is called during `__init__` and before data store lookups. |
| **Whitespace-only names**<br>e.g., `Patient("P1", "   ")` or `Practitioner("DR1", "   ", "GP")` | The system raises a `ValueError` and rejects the whitespace-only string. The object is not created. | **Contract:** `required_text()` in `domain.py`.<br>*Code:* Explicitly strips and checks `if not value.strip()`, ensuring invisible blank names cannot be registered. |
| **Same-time practitioner bookings**<br>e.g., Booking "DR1" for "2026-10-01 09:00" when that slot is already taken by another SCHEDULED appointment. | The first booking succeeds. The second booking attempt raises a `ValueError` ("Practitioner already has a SCHEDULED appointment..."). | **Contract:** `AppointmentService.book_appointment()` and `SmartCareDataStore.has_practitioner_conflict()`.<br>*Code:* The service checks for conflicts before calling `add_appointment()`, ensuring the store is not mutated on failure. |
| **Cancelled appointments**<br>e.g., Attempting to book a slot that was previously booked but has since been cancelled, or trying to cancel a COMPLETED appointment. | The system **allows** a new booking at that same time. A cancelled appointment remains in the store but no longer blocks the schedule. | **Contract:** `SmartCareDataStore.has_practitioner_conflict()`.<br>*Code:* The conflict check explicitly filters for `appointment.status is AppointmentStatus.SCHEDULED`, meaning `CANCELLED` records are ignored during conflict checks but retained in the list. |
| **Invalid status transitions**<br>e.g., Calling `cancel()` on an appointment that is already `CANCELLED` or `COMPLETED`. | The system raises a `ValueError` ("Only SCHEDULED appointments may be cancelled") and leaves the status unchanged. | **Contract:** `Appointment.cancel()` in `domain.py`.<br>*Code:* The method guards the transition: `if self.status is not AppointmentStatus.SCHEDULED: raise ValueError(...)`. |
### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | [response] | [response] |
| 2 | [response] | [response] |
| 3 | [response] | [response] |
| 4 | [response] | [response] |
| 5 | [response] | [response] |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
[response]

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [complete]
Acceptance criterion: [quote]
Behaviour to test: [complete]
Human-first test idea/categories: [complete]
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[response]

2. What question does validation answer?
[response]

3. What is a unit test?
[response]

4. What is a pytest fixture?
[response]

5. What is parametrisation in pytest?
[response]

6. What is regression testing?
[response]

7. What does code coverage tell us, and what does it not prove?
[response]

8. What makes an assertion weak?
[response]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
