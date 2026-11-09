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

Response and reason: The statement "Appointment disappears after cancellation" is a symptom because it describes the problem being experienced. "The data-store removal path is probably being called" is a hypothesis because it suggests a possible cause without confirmed evidence. The statement showing that store.find_appointment('A1') returns None is evidence, as it provides an observable test result. "The service layer is badly designed" is an opinion, since it makes a judgement without supporting facts. Finally, the traceback pointing to smartcare/services.py is evidence because it identifies where an error occurred, although it does not necessarily identify the root cause.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: For this activity, we investigated cancelled appointments becoming inaccessible after cancellation. According to FR-07 and FR-08, cancelled appointments should remain stored and retrievable. However, our tests showed that cancelling appointment A1 caused find_appointment() to return None. We reproduced the issue by registering patient P1 and practitioner D1, booking appointment A1, cancelling it and attempting to retrieve it. Our initial hypothesis was that the lookup method incorrectly excluded cancelled appointments. To investigate this, we planned to compare find_appointment() with list_appointments() to determine whether the appointment was deleted or simply filtered out.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: A test expecting cancelled appointments to be deleted would be incorrect because FR-07 requires appointment history to be retained. Therefore, the test should be corrected rather than changing the application to remove cancelled appointments. Similarly, AC-04.2 allows different practitioners to have appointments at the same time, meaning a test expecting this situation to cause a conflict would also be incorrect. These examples demonstrate why test expectations must be checked against the requirements before modifying the code.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: The hypothetical AppointmentService method contains several code smells, including duplicated status strings, excessive nesting, unclear responsibilities and direct manipulation of stored collections. These could be improved by extracting repeated logic into helper methods, using the existing AppointmentStatus enum, simplifying conditional statements and moving collection operations into SmartCareDataStore. Renaming appt to appointment, extracting a repeated conflict helper and replacing hardcoded status strings are examples of refactoring because they improve code structure without changing behaviour. Restoring cancelled appointment lookup is a bug repair, while adding rescheduling is a new feature. Any refactoring must preserve existing validation, booking, cancellation and lookup behaviour.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: During testing, test_service_cancel_appointment failed at tests/test_services.py:129 with an AttributeError because find_appointment('A1') returned None instead of the cancelled appointment. This contradicted FR-07 and FR-08, which require appointment history to remain accessible. The relevant call path involved the test calling the data-store lookup, which searched list_appointments() and applied a status condition. We considered three possible causes: an incorrect filter in find_appointment() (most likely), cancellation removing the appointment from storage (second), and list_appointments() excluding cancelled appointments (third). We distinguished these explanations by checking the lookup conditions and confirming that the cancelled appointment remained in the stored collection. This demonstrated that the traceback identified the failure, but inspecting the code and stored objects was necessary to confirm the root cause.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: Changing code immediately after encountering a failure can be a poor debugging strategy because the cause of the problem may not yet be understood. This can lead to unnecessary changes, incorrect fixes or additional defects. A better approach is to reproduce the failure, compare the observed behaviour with the requirements, form a hypothesis and examine evidence before making changes. Our Stage 8 investigation demonstrated this process by identifying the causes of both defects before repairing them.


Classification responses (1–5, each with reason): The first statement is a symptom because it describes an appointment disappearing after cancellation. The second is a hypothesis because it suggests that the data-store removal process is responsible without providing evidence. The third is evidence because the failing test confirms that find_appointment('A1') returns None. The fourth is an opinion because it criticises the service layer without identifying a specific problem. Finally, the fifth is evidence because a traceback identifies where an error was observed, although this does not necessarily prove its cause.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: We investigated the issue of cancelled appointments becoming inaccessible. According to FR-07 and FR-08, cancelled appointments should remain stored and retrievable. However, our tests showed that retrieving appointment A1 after cancellation returned None. We reproduced the issue by registering patient P1 and practitioner D1, booking A1, cancelling it and attempting to retrieve the appointment. Our hypothesis was that find_appointment() incorrectly excluded cancelled appointments. To investigate this, we compared the lookup method with list_appointments() to determine whether the appointment had been deleted or was simply being filtered out.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: The test test_service_cancel_appointment failed at tests/test_services.py:129 with an AttributeError because find_appointment('A1') returned None instead of the retained appointment with CANCELLED status. This contradicted FR-07 and FR-08. The call path involved the test calling SmartCareDataStore.find_appointment(), which used list_appointments() before applying a status condition. We ranked an incorrect lookup filter as the most likely cause, followed by appointment deletion and filtering within list_appointments(). We distinguished these possibilities by inspecting the lookup condition and checking whether the cancelled appointment remained in storage. The regression test confirmed that A1 was still listed, identifying the lookup filter as the root cause.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: d576e06be2c22b5f10bd83abe2b501d837976cf9 — Assignment 3 revision 2 requirements.
- Baseline test command / working directory / observed result / evidence: Ran python -m pytest -q from project/. All 29 tests passed in 0.03 seconds.
- Clean preparation SHA if a record-only commit followed Stage 7: n/a
- Branch and preparer / how teammates obtained this branch: debug/stage8, prepared by u3334274.
- Downloaded tool version, source SHA256 and --check outcome: Stage 8 utility version 1.1. Preflight PASS. Baseline SHA256: b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375. Both fault signatures verified in a temporary copy; project unchanged.
- --apply and --verify output summaries / artefact references: The preparation utility introduced the two controlled defects in data_store.py. Subsequent testing reproduced both the practitioner conflict and cancelled appointment lookup failures.
- Bounded diff inspected and recovery location (not committed): Only project/smartcare/data_store.py was modified, with 11 insertions and 18 deletions. Local recovery metadata is stored in project/.stage8_faults/ and should remain excluded from Git.
- Prepared faulty-state commit SHA: cf9495a — Prepare Stage 8 debugging faults.
- Preparation or recovery issues and resolution, if any: nitially, the preparation script could not be located. After obtaining it and placing it outside the repository in Stage_8_Assets, the preparation check passed. No restoration was required.
- Initial prepared full-suite command / result / key failures: Ran python -m pytest -q from project/. Result: 26 passed, 3 failed in 0.05 seconds. The failures involved practitioner booking conflicts and cancelled appointment lookup.

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: Conflicting booking was accepted
- Expected behaviour and requirement: Same-practitioner/time booking rejected
- Minimal synthetic reproduction steps: Register patients P1/P2 and practitioner D1. Book A1 with D1 at 2026-10-01 09:00, then attempt A2 with D1 at the same time. The second booking is incorrectly accepted instead of raising ValueError.
- Meaningful failing test path/name and exact relevant failure: tests/test_starter.py::test_conflict_rule_and_different_practitioner
Failure: Failed: DID NOT RAISE ValueError (line 127).
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: The has_practitioner_conflict() method incorrectly used != when comparing practitioner IDs. The regression test confirmed that this allowed conflicting appointments to be booked.
- Smallest justified fix / diff / why other behaviour is preserved: Changed the practitioner comparison from != to ==, ensuring that only matching practitioners at the same time trigger a conflict. Other booking conditions remain unchanged.
- Repair SHA / focused verification result: The F8-01 regression test passed after repair. The full suite passed all 31 tests. Repair SHA: 9770048 — Corrected the practitioner comparison

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: Cancelled appointment could not be found
- Expected behaviour and requirement: Cancelled appointment remains retrievable
- Minimal synthetic reproduction steps: Register P1 and D1, book A1, then cancel it. Attempting to retrieve A1 returns None despite its cancellation status. Repeated cancellation also fails with the wrong exception.
- Meaningful failing test path/name and exact relevant failure: tests/test_services.py::test_service_cancel_appointment
Failure: AttributeError: 'NoneType' object has no attribute 'status' (line 129). tests/test_services.py::test_service_repeated_cancellation_rejected
Failure: LookupError: Appointment not found (line 151).
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: The find_appointment() method excluded appointments with a cancelled status. Testing confirmed the appointment remained stored, but lookup incorrectly returned None.
- Smallest justified fix / diff / why other behaviour is preserved: Restored direct dictionary lookup using required_text(), removing the cancelled-status restriction while retaining ID validation and existing object identity.
- Repair SHA / focused verification result: The F8-02 regression test passed after repair. The full suite passed all 31 tests. Repair SHA: 9770048 — Corrected the practitioner comparison

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
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot correctly identified that find_appointment() excludes cancelled appointments. The regression test confirms the original appointment remains stored, but lookup returns None. We accepted this explanation because it matches the code and observed failure.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that cancellation might delete the appointment. However, the assertion original in store.list_appointments() passed after cancellation, confirming the appointment remains stored. Therefore, we rejected this explanation.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that list_appointments() might hide cancelled appointments. However, the same assertion passed, and the method returns all stored objects without filtering. Therefore, we rejected this suggestion.
Final human conclusion and comparison with initial hypothesis: The root cause is the cancelled-status restriction inside find_appointment(). Removing this restriction will restore access to cancelled appointments while preserving their status and object identity.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|--|--|--|
| F8-01 before repair | Faulty != practitioner comparison | python -m pytest tests/test_regressions.py -v | FAILED — DID NOT RAISE ValueError |
| F8-01 after repair | Corrected to == |  python -m pytest tests/test_regressions.py -v | PASSED |
| F8-02 before repair | Cancelled status excluded from lookup |  python -m pytest tests/test_regressions.py -v | FAILED — assert None is <Appointment object> |
| F8-02 after repair | Restored validated dictionary lookup |  python -m pytest tests/test_regressions.py -v | PASSED |
| Full suite after both repairs, before refactor | Repaired code; SHA to record | python -m pytest -q | 	31 passed, 0 failed |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: F8-01 verifies that conflicting bookings are rejected without changing stored appointments, while different practitioners can still be booked. F8-02 confirms cancelled appointments remain stored and retrievable, and repeated cancellation is rejected.
Unrelated failures investigated / resolution: Not applicable. The three initial test failures were associated with the two prepared Stage 8 defects, and all 31 tests passed after the repairs.

## H. Refactoring decision and before/after verification

Smell and exact location: has_practitioner_conflict() in smartcare/data_store.py contains a lengthy conditional expression that is difficult to read.
Small proposed structural change / why justified: Separate the practitioner, time and status comparisons into clearly named Boolean variables to improve readability without altering the existing logic.
External behaviour to preserve / relevant tests: The system must continue rejecting conflicting practitioner bookings while allowing different practitioners and preserving cancelled appointment history. Existing regression tests will verify this behaviour.
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: Changed appointment.status.value == "scheduled" to appointment.status is AppointmentStatus.SCHEDULED. Commit SHA: 9770048
Focused and full after-refactor commands / working directory / results / evidence: Ran python -m pytest tests/test_regressions.py -v and python -m pytest -q from project/. Both regression tests passed, and the full suite passed.
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: Accepted. The change improves code readability without altering the expected behaviour. Passing regression tests confirm that the previously repaired booking conflict and cancelled appointment lookup defects have not returned.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: F8-01: Practitioner conflict correction — u3334274.
F8-02: Cancelled appointment lookup correction — u3334274.
Refactor: Simplify conditional logic — [confirm owner].
Issue links: [Add actual GitHub issue links].
Branch / prepared, repair and refactor checkpoints: Branch: debug/stage8. Prepared faulty-state SHA: cf9495a. Repair SHA: 9770048. Refactor SHA: 8b2ced6.
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: The reviewer examined the two bug repairs, regression tests and refactoring to confirm they followed the SmartCare requirements. Unlike Copilot's initial diagnosis, which considered several possible causes, the human review focused on whether the implemented repairs were minimal and supported by the test evidence.
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: u3334274 (Seb): Debugging preparation, human diagnoses, regression testing, repairs and Copilot evaluation.
u3323819 (Deng): [Insert verified contribution and link].
u3324852 (Ryan): [Insert verified contribution and link].

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? Copilot suggested that the booking service might not call the practitioner conflict checker. Although initially plausible, inspecting book_appointment() confirmed that the method was called correctly, so we rejected the explanation.
2. What evidence changed your group's view? The regression tests and code inspection helped distinguish the actual causes from alternative explanations. In particular, F8-02 testing confirmed that the cancelled appointment remained stored, proving the problem was lookup filtering rather than deletion.
3. How did regression tests protect the refactoring? The regression tests establish the correct booking and cancellation behaviour before refactoring. Repeating them afterwards will help confirm that structural improvements have not reintroduced either defect or changed existing functionality.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Reproduce the failure, identify expected behaviour, form a hypothesis and inspect evidence to determine the likely cause.

2. Where should expected behaviour come from during debugging?

Response: Expected behaviour should come from the system requirements, acceptance criteria and documented business rules.

3. What is a debugging hypothesis?

Response: A testable explanation for why a particular failure is occurring.

4. What is a regression test and why is it retained?

Response: A test that checks previously working or repaired behaviour to prevent the same defect from returning after future changes.

5. What is meant by root cause?

Response: The underlying problem responsible for producing the observed failure.

6. What is refactoring?

Response: Improving the structure or readability of code without changing its external behaviour.

7. What is a swallowed exception?

Response: An exception that is caught and ignored, hiding errors rather than allowing them to be handled properly.

8. What is a code smell?

Response: A characteristic of code that suggests potential problems with readability, maintainability or design.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: As suggestions that must be evaluated against actual code, tests and requirements rather than automatically accepted.

10. What is the Stage 8 engineering rule?

Response: Diagnose before you fix. Understand and reproduce the problem before making changes, then verify repairs with meaningful tests.

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