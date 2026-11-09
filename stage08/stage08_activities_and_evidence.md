# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [Group 5]
Members and UG/PG cohorts: [u3323819 (Deng), u3334274 (Seb), u3324852 (Ryan)]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [complete]
- Baseline test command / working directory / observed result / evidence: [complete]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: Conflicting booking was accepted
- Expected behaviour and requirement: Same-practitioner/time booking rejected
- Minimal synthetic reproduction steps: Register patients P1/P2 and practitioner D1. Book A1 with D1 at 2026-10-01 09:00, then attempt A2 with D1 at the same time. The second booking is incorrectly accepted instead of raising ValueError.
- Meaningful failing test path/name and exact relevant failure: tests/test_starter.py::test_conflict_rule_and_different_practitioner
Failure: Failed: DID NOT RAISE ValueError (line 127).
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: Cancelled appointment could not be found
- Expected behaviour and requirement: Cancelled appointment remains retrievable
- Minimal synthetic reproduction steps: Register P1 and D1, book A1, then cancel it. Attempting to retrieve A1 returns None despite its cancellation status. Repeated cancellation also fails with the wrong exception.
- Meaningful failing test path/name and exact relevant failure: tests/test_services.py::test_service_cancel_appointment
Failure: AttributeError: 'NoneType' object has no attribute 'status' (line 129). tests/test_services.py::test_service_repeated_cancellation_rejected
Failure: LookupError: Appointment not found (line 151).
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: The practitioner conflict check uses != instead of ==, causing the system to check different practitioners rather than the same practitioner.
Evidence intended to inspect / competing explanation / discriminating check: Inspect has_practitioner_conflict() and compare bookings with the same and different practitioners. Check whether the issue originates in the service or data-store logic.
Member and saved sequence/time or commit showing this preceded consultation: u3334274 — Diagnosis recorded before GitHub Copilot consultation. 2026-11-06 15:05:44 AEDT

### F8-02 human entry
Likely cause and why plausible: The find_appointment() method excludes cancelled appointments, causing lookup to return None even though the appointment remains stored.
Evidence intended to inspect / competing explanation / discriminating check: Compare find_appointment() with list_appointments() after cancellation to determine whether the appointment was deleted or incorrectly filtered.
Member and saved sequence/time or commit showing this preceded consultation: u3334274 — Diagnosis recorded before GitHub Copilot consultation. 2026-11-06 15:05:44 AEDT

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: I am completing Stage 8 (Debugging and Refactoring) of my SmartCare Python assignment. I have identified a defect involving practitioner appointment conflicts. Observed behaviour: The system incorrectly allows two appointments to be booked for the same practitioner at the same date and time. Expected behaviour: The system should reject a second SCHEDULED appointment for the same practitioner and time by raising ValueError. Different practitioners should be allowed appointments at the same time. 

Steps to reproduce: Register patients P1 and P2 and practitioners D1 and D2. Book appointment A1 with practitioner D1 at 2026-10-01 09:00. Attempt to book A2 with D1 at the same time. Observe that the conflicting booking is accepted. 

Failing test: tests/test_regressions.py::test_f8_01_practitioner_conflict 

Exact failure: Failed: DID NOT RAISE ValueError (line 29). My hypothesis: The practitioner conflict check may be using an incorrect comparison operator. In has_practitioner_conflict(), the practitioner IDs are compared using != instead of ==.

Relevant code:
def has_practitioner_conflict(
    self,
    practitioner_id: str,
    date_time: datetime,
    exclude_appointment_id: str | None = None,
) -> bool:
    for appointment in self.list_appointments():
        if (appointment.appointment_id != exclude_appointment_id
                and appointment.practitioner.practitioner_id != practitioner_id
                and appointment.date_time == date_time
                and appointment.status.value == "scheduled"):
            return True
    return False

Task: Rank the three most likely causes of this defect, from most likely to least likely. For each possible cause: Explain why it could produce the observed failure. Identify specific code or test evidence I should inspect to confirm or reject it. Explain how to distinguish it from the other possible causes. Do not rewrite the entire application, implement fixes or invent requirements. Treat all suggested explanations as hypotheses rather than confirmed facts.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot correctly identified that has_practitioner_conflict() uses != instead of ==. This causes the system to check for different practitioners rather than matching ones, allowing conflicting bookings. We accepted this suggestion because it directly explains the failing test.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that the conflict detection method might not be called during booking. However, inspecting book_appointment() confirmed that it calls has_practitioner_conflict() and raises a ValueError when a conflict is detected. Therefore, we rejected this explanation.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that the appointment status comparison might prevent conflicts from being detected. However, AppointmentStatus.SCHEDULED.value is "scheduled", which matches the condition in the method. Therefore, we rejected this suggestion.
Final human conclusion and comparison with initial hypothesis: The root cause of F8-01 is the incorrect practitioner comparison operator in data_store.py. Changing != to == should restore correct conflict detection without affecting other booking rules.

### F8-02 Copilot review
Actual prompt / output reference and member: I am completing Stage 8 (Debugging and Refactoring) of my SmartCare Python assignment. I have identified a defect involving cancelled appointment history. Observed behaviour: After cancelling an appointment, the data-store lookup returns None even though the appointment should remain stored. Attempting to cancel it again raises LookupError instead of the expected ValueError. Expected behaviour: Cancelling an appointment should change its status to CANCELLED without deleting it. The same appointment object should remain accessible through lookup and listing. Repeated cancellation should raise ValueError.

Steps to reproduce: Register patient P1 and practitioner D1. Book appointment A1 for 2026-10-01 09:00. Cancel appointment A1. Attempt to retrieve A1 using find_appointment("A1"). Observe that the lookup returns None.

Failing test: tests/test_regressions.py::test_f8_02_cancelled_appointment_retained 

Exact failure: AssertionError: assert None is <smartcare.domain.Appointment object ...> (line 60). My hypothesis: The data-store lookup incorrectly filters out cancelled appointments, preventing them from being retrieved.

Relevant code:
def find_appointment(self, appointment_id: str) -> Appointment | None:
    if not isinstance(appointment_id, str) or not appointment_id.strip():
        raise ValueError("Appointment ID cannot be blank")
    for appointment in self.list_appointments():
        if (appointment.appointment_id == appointment_id.strip()
                and appointment.status.value != "cancelled"):
            return appointment
    return None

Task: Rank the three most likely causes of this defect, from most likely to least likely. For each possible cause: Explain why it could produce the observed failure. Identify specific code or test evidence I should inspect to confirm or reject it. Explain how to distinguish it from the other possible causes. Do not rewrite the entire application, implement fixes or invent requirements. Treat all suggested explanations as hypotheses rather than confirmed facts.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot correctly identified that find_appointment() excludes appointments with a "cancelled" status. This explains why the lookup returns None even though the appointment still exists. We accepted this suggestion because it directly matches the code and failing regression test.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that cancellation might delete appointments from storage. However, the regression test confirms that the original appointment object is successfully cancelled, while the data store's list_appointments() method returns all stored appointments without filtering. The evidence points to a lookup issue rather than deletion, so we rejected this explanation.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that list_appointments() might exclude cancelled appointments. However, inspecting the method confirms that it returns all stored appointment objects using list(self._appointments.values()), without filtering by status. Therefore, we rejected this suggestion.
Final human conclusion and comparison with initial hypothesis: The root cause of F8-02 is the incorrect status restriction in find_appointment(). Removing this restriction will allow cancelled appointments to remain accessible while preserving their original status and object identity.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
