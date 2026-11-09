# Stage 12 – UG Release Activities and Evidence

**Project:** SmartCare
**Assessment:** Software Technology 1 – Assignment 3
**Pathway:** Undergraduate (UG)
**Group members:** Deng, Seb and Ryan
**Stage 12 owner:** Deng
**Repository:** https://github.com/ShadowMonrch/st1-assignment-3
**Release branch:** release/stage12-ug
**Final tested commit:** 9b10a5d4f75cdb45a10464cc5d224ea5739ae7f9
**Commit message:** docs: update UG release README and remove empty file
**Date of record:** 9 November 2026

---

## A. Release scope and starting point

The purpose of Stage 12 was to prepare and review the SmartCare Undergraduate release. This involved checking the implemented functionality, running regression tests, demonstrating the application, reviewing the documentation, and recording the release evidence.

The group followed the UG pathway. The completed development stages were:

- Stage 6 – Shared starter implementation, Mostly completed by Deng as he created the repository.
- Stage 7 – Implementation work completed by Ryan.
- Stage 8 – Implementation work completed by Seb.
- Stage 9 – Query implementation and integration work completed by Ryan.
- Stage 12 – UG release preparation and evidence completed by Deng.

Stages 10 and 11 are postgraduate-only stages and are not part of this group's UG pathway. Their original templates have been retained unchanged.

**Repository:** https://github.com/ShadowMonrch/st1-assignment-3

**Release branch:** release/stage12-ug

**Starting point:** 2b6fdf498b99e1d4557c678627c4627aadc5ed22

**Stage 9 merge commit:** da07a8dfbfea8110250d60fd0d58747247ec6d40

**Final Stage 12 commit:** 9b10a5d4f75cdb45a10464cc5d224ea5739ae7f9

The release work included checking the existing implementation, running the automated tests, demonstrating the interactive application, updating the project README, and removing an empty tracked file.

A formal feature-freeze date was not separately recorded.

## B. Release readiness matrix

The following matrix records the status of the main release activities.

| Area | Status | Evidence / comments |
|---|---|---|
| Core implementation | Completed | Main SmartCare functionality implemented across the domain, data store and service modules. |
| Patient registration | Completed | Registration and lookup functionality tested. |
| Practitioner registration | Completed | Practitioner registration and lookup functionality tested. |
| Appointment booking | Completed | Booking functionality and validation tested. |
| Appointment cancellation | Completed | Cancellation state transition tested. |
| Appointment queries | Completed | Practitioner and status filtering tested. |
| Appointment sorting | Completed | Query tests verify ascending ordering. |
| Automated regression testing | Completed | Full test suite: 52 passed. |
| Interactive demonstration | Completed | Interactive application manually demonstrated. |
| Documentation review | Completed | Project README updated and release documentation reviewed. |
| Peer review | Completed | Ryan checked the work and verbally approved it in person. |
| Root README completion | Completed | Group 8 details, member usernames, repository URL, tested SHA and test results recorded. |
| Fresh-clone verification | Outstanding | A fresh clone has not been independently verified as part of this evidence. |
| Final source ZIP | Outstanding | Final ZIP creation and extraction testing have not been recorded. |
| Final submission package verification | Outstanding | Final package contents and submission details still require confirmation. |

The automated tests and manual demonstration provide evidence that the implemented functionality is working. However, the outstanding packaging and documentation checks should be completed before treating the submission package as fully verified.

## C. Regression testing

Regression testing was completed using pytest to check that the existing functionality continued to work after the Stage 12 release preparation.

The full test suite was executed from the project directory.

**Command:**

```powershell
python -m pytest -q
```

**Result:**

```text
52 passed
```

The focused test groups were also executed:

| Test file | Result |
|---|---:|
| tests/test_queries.py | 8 passed |
| tests/test_services.py | 23 passed |
| tests/test_workflows.py | 3 passed |
| Full test suite | 52 passed |

The tests covered the main domain, service, query and workflow functionality.

The regression checks included:

- Patient and practitioner registration.
- Patient and practitioner lookup.
- Appointment booking.
- Appointment cancellation.
- Validation of invalid inputs.
- Prevention of duplicate or conflicting appointments.
- Appointment filtering by practitioner.
- Appointment filtering by status.
- Appointment ordering.
- End-to-end appointment workflows.

The full suite was rerun after the final Stage 12 commit and reported 52 passing tests.

**Tested commit:**

9b10a5d4f75cdb45a10464cc5d224ea5739ae7f9

No test failures were reported in the final run.

## D. Application demonstration

The SmartCare application was manually demonstrated using its interactive console.

**Command:**

```powershell
python main.py --interactive
```

The demonstration was performed from the project directory.

The following test data and scenarios were used.

### Demonstration data

| Record | Details |
|---|---|
| Patient | P100 – Alex Morgan |
| Practitioner | DR100 – Dr Sarah Chen, General Practice |
| Practitioner | DR101 – Dr James Wilson, Cardiology |
| Appointment | A100 |
| Appointment | A101 |
| Appointment | A102 |

### Demonstration activities

**1. Patient and practitioner lookup**

The application was used to locate the registered patient and practitioners. The expected records were returned.

**2. Successful appointment booking**

Appointment A100 was booked for patient P100 with practitioner DR100 at:

2026-11-12 10:00

The booking was accepted.

**3. Practitioner scheduling conflict**

A second appointment, A101, was attempted with the same practitioner at the same scheduled time.

The application rejected the booking because the practitioner already had a scheduled appointment at that time.

**4. Booking with another practitioner**

Appointment A102 was booked at the same time with practitioner DR101.

The booking was accepted because it did not conflict with the other practitioner's schedule.

**5. Appointment cancellation**

Appointment A100 was cancelled successfully.

The appointment could subsequently be found with its status displayed as cancelled.

**6. Repeated cancellation**

A second attempt to cancel A100 was rejected because the appointment was already cancelled.

**7. Appointment listing and filtering**

The practitioner appointment listing was checked.

The DR100 listing included A100 when displaying all appointments. Filtering by scheduled status did not include the cancelled appointment, while filtering by cancelled status returned A100.

The DR101 listing returned A102 as a scheduled appointment.

**8. Invalid input handling**

The application was tested with an invalid menu selection, an unknown patient identifier and an invalid date value.

The application displayed appropriate error messages and allowed the user to continue using the menu.

**9. Application exit**

The application was exited using menu option 0.

The demonstration also showed that the application uses in-memory storage, meaning that records created during a session are not permanently retained after the program closes.

The manual demonstration supported the automated test results by showing the main user-facing workflows operating through the interactive console.

## E. Code quality and AI review

The Stage 12 code review focused on the main application structure, readability, validation, error handling and consistency between the implemented functionality and the intended SmartCare workflows.

The following modules were reviewed:

| File | Review focus |
|---|---|
| smartcare/domain.py | Domain models, attributes, validation and appointment status. |
| smartcare/data_store.py | In-memory storage, registration, lookup and appointment conflict checks. |
| smartcare/services.py | Registration, booking, cancellation and appointment service operations. |
| smartcare/queries.py | Appointment filtering and sorting. |
| smartcare/console.py | Interactive menu, input handling and user-facing error messages. |
| main.py | Application entry point and command-line execution. |
| requirements-dev.txt | Development dependency configuration. |

### Review findings

The implementation separates the domain models, data storage, service operations, queries and console interface into different modules.

This structure makes the application easier to understand and maintain because each module has a defined responsibility.

The review also considered:

- Whether invalid input is handled appropriately.
- Whether appointment cancellation changes the appointment status correctly.
- Whether appointment conflicts are prevented.
- Whether query operations return the expected results.
- Whether the interactive application can recover from invalid user input.
- Whether the project documentation explains how to run the application.

No release-blocking defect was identified in the reviewed modules.

The review was supported by the automated test results and manual demonstration. It was not a formal static-analysis audit or a comprehensive security assessment.

### AI assistance

Copilot was used as an assistance tool.

Its use included:

- Helping find out the root cause of a problem


## F. README and reproducibility

The project documentation was reviewed and the project-level README was updated.

The project README provides information about the SmartCare application, its purpose, requirements and execution.

The development dependency file is:

project/requirements-dev.txt

It specifies:

```text
pytest==8.3.5
```

### Running the application

From the project directory:

```powershell
python main.py
```

The interactive application can be launched using:

```powershell
python main.py --interactive
```

### Running the tests

From the project directory:

```powershell
python -m pytest -q
```

The final recorded result was:

```text
52 passed
```

### Reproducibility considerations

The project uses Python and pytest. The test environment used for the recorded final run was Python 3.13.14 with pytest 8.3.5 on Windows.

The application uses in-memory data storage. Therefore, records created during an interactive session are not saved permanently.

The project README and root repository README have been updated. The root README includes the group information, repository URL, tested SHA and regression test results. A fresh clone and a final source ZIP extraction test have not been recorded as completed.

## G. Limitations, technical debt and release notes

### Current limitations

The SmartCare implementation has several limitations that should be considered when evaluating the release.

**1. In-memory storage**

The application stores information in memory rather than a persistent database. Patient, practitioner and appointment records are not retained after the program closes.

**2. Console-based interface**

The application uses an interactive command-line interface rather than a graphical user interface or web application.

**3. No authentication system**

The current implementation does not include a complete user authentication or role-based access control system.

**4. No external integrations**

The application does not currently integrate with external healthcare systems, notification services or third-party scheduling platforms.

**5. Limited production readiness**

The implementation is an educational project and is not intended to be deployed as a production healthcare management system.

### Technical debt and future improvements

Possible future improvements include:

- Implementing persistent database storage.
- Introducing authentication and role-based access control.
- Developing a graphical or web-based interface.
- Improving audit logging.
- Adding automated notifications and reminders.
- Expanding validation and edge-case testing.
- Improving deployment and configuration management.

### Release notes

The Stage 12 release preparation included:

- Reviewing the existing SmartCare implementation.
- Running the full automated test suite.
- Demonstrating the interactive application.
- Reviewing the project documentation.
- Updating the project README.
- Removing an empty tracked file.
- Recording the final tested commit.

The release retains the existing in-memory architecture and console interface.

## H. Release findings and defect review

The Stage 12 review considered the implementation, tests, documentation and repository contents.

### Findings

| Finding | Severity | Action / outcome |
|---|---|---|
| Project README required updating | Documentation issue | Updated during Stage 12. |
| Empty tracked project/testing123.py file | Repository cleanup | Removed in the Stage 12 documentation/cleanup commit. |
| Root README contained incomplete placeholders | Documentation issue | Completed during Stage 12 by adding the group information, repository URL, tested SHA and test results. |
| Application uses in-memory storage | Known limitation | Recorded as a project limitation. |
| No fresh-clone verification recorded | Release evidence gap | Still requires verification. |
| No final ZIP extraction test recorded | Release evidence gap | Still requires verification. |

The empty project/testing123.py file was removed as part of the final cleanup commit.

The automated test suite reported 52 passing tests, and the manual demonstration successfully exercised the main workflows.

No release-blocking software defect was identified during the reviewed activities.

The remaining issues are primarily related to documentation and final submission-package verification rather than a known failure of the tested application functionality.

## I. Git review and integration

The shared GitHub repository was used for the group's development and integration work.

**Repository URL:**

https://github.com/ShadowMonrch/st1-assignment-3

**Release branch:**

release/stage12-ug

### Git history

The recorded integration history includes:

| Event | Commit |
|---|---|
| Starting point from origin/main | 2b6fdf498b99e1d4557c678627c4627aadc5ed22 |
| Stage 9 merge | da07a8dfbfea8110250d60fd0d58747247ec6d40 |
| Final Stage 12 commit | 9b10a5d4f75cdb45a10464cc5d224ea5739ae7f9 |

The final commit message was:

docs: update UG release README and remove empty file

The release branch was recorded as seven commits ahead of origin/main at the time of the repository review.

### Peer review

Ryan checked the SmartCare work with Deng in person. He reviewed the completed work and verbally confirmed that he was satisfied with it and approved it.

This is recorded as an in-person peer review and verbal approval by another group member.

Ryan's review provided an additional group-member check alongside Deng's own code inspection, regression testing and release preparation.

No separate written approval record was created, and the approval should not be interpreted as formal tutor sign-off.

## J. Human release decision

The Stage 12 release decision considered the results of the regression tests, the manual application demonstration, the code review and Ryan's in-person peer approval.

### Review outcome

The application passed the recorded automated regression tests, with 52 tests passing.

The manual demonstration also showed that the main appointment workflows operated as expected, including successful booking, conflict prevention, cancellation, filtering and invalid input handling.

Ryan checked the work in person and verbally approved it.

### Release decision

The reviewed SmartCare implementation is suitable to be presented as the group's UG Stage 12 release candidate based on the evidence recorded above.

However, the complete submission package should not be described as fully verified until the remaining documentation and packaging checks are completed.

The following items remain outstanding:

- Verifying the final repository state.
- Creating the final source ZIP.
- Extracting the ZIP into a clean location.
- Running the application and test suite from the extracted package.
- Confirming the final submission package contents.

**Stage 12 owner:** Deng

**Peer reviewer:** Ryan

**Approval method:** In-person review and verbal approval.

**Written approval record:** Not separately created.

**Tutor approval:** Not recorded.

## K. Final tested SHA

The final tested commit recorded for the Stage 12 release is:

```text
9b10a5d4f75cdb45a10464cc5d224ea5739ae7f9
```

**Commit subject:**

```text
docs: update UG release README and remove empty file
```

The full regression suite was rerun after this commit and reported:

```text
52 passed
```

The manual demonstration was also completed using the interactive application.

The tested SHA should be checked against the repository's actual HEAD before final submission to ensure that no later changes have been made.

No final source ZIP SHA or separate package checksum has been recorded.

## L. Final submission package verification

The following checklist records the status of the submission package.

| Verification item | Status |
|---|---|
| Correct shared GitHub repository identified | Completed |
| UG release branch identified | Completed |
| Final tested SHA recorded | Completed |
| Full automated test suite executed | Completed |
| Manual application demonstration completed | Completed |
| Project README updated | Completed |
| Root README placeholders completed | Completed |
| Original UG and PG stage templates retained | Completed |
| Final source ZIP created | Outstanding |
| ZIP extracted into a clean location | Outstanding |
| Application run from extracted ZIP | Outstanding |
| Tests run from extracted ZIP | Outstanding |
| Final package contents checked | Outstanding |
| Final submission package confirmed | Outstanding |

### Submission package considerations

The final submission should include the SmartCare source code, the relevant test files, the required documentation and the completed UG Stage 12 evidence.

The original PG Stage 10 and Stage 11 templates should remain unchanged because the group followed the UG pathway.

The final source package should exclude unnecessary local development artefacts such as virtual environments and pytest cache files.

A final package verification should be performed after the remaining documentation has been completed.

## M. Formative questions

### 1. What is the purpose of the domain layer?

The domain layer defines the main objects and rules used by the application. In SmartCare, it contains entities such as patients, practitioners and appointments, along with appointment statuses and validation.

### 2. Why is the application separated into different modules?

Separating the application into modules improves organisation and maintainability. Each module has a different responsibility, such as storing data, handling business logic, performing queries or interacting with the user.

### 3. What is the responsibility of the data store?

The data store manages the application's in-memory records. It supports registering and retrieving patients and practitioners and storing appointment information.

### 4. How does SmartCare prevent appointment conflicts?

The application checks whether a practitioner already has a scheduled appointment at the requested time. If a conflicting scheduled appointment exists, the new booking is rejected.

### 5. What happens when an appointment is cancelled?

The appointment's status changes to cancelled. The appointment remains available for lookup, but it is no longer treated as a scheduled appointment.

### 6. Why are automated tests important?

Automated tests help verify that the application behaves as expected. They also help identify regressions when code is changed or new functionality is integrated.

### 7. What is regression testing?

Regression testing checks that previously implemented functionality continues to work after changes are made to the application.

### 8. What is the purpose of the query module?

The query module retrieves appointments based on specified criteria. In SmartCare, appointments can be filtered by practitioner and status and sorted by date and appointment identifier.

### 9. What are the limitations of the current SmartCare implementation?

The current application uses in-memory storage and a console-based interface. It does not have persistent database storage, a complete authentication system or external healthcare integrations.

### 10. What would be the next improvement to SmartCare?

A useful next improvement would be implementing persistent database storage. This would allow patient, practitioner and appointment records to remain available after the application closes. Additional improvements could include authentication, role-based permissions and a graphical interface.

## N. Reflection, viva preparation and handover

### Reflection

My main responsibility during Stage 12 was preparing and reviewing the SmartCare UG release evidence.

I reviewed the main application modules, checked the repository structure, ran the automated regression tests and manually demonstrated the interactive application.

The testing process helped confirm that the main functionality was working as expected. The full test suite reported 52 passing tests, and the manual demonstration successfully exercised important appointment workflows.

I also reviewed the project documentation and updated the project README. The review identified remaining documentation and packaging tasks that need to be completed before the final submission package can be considered fully verified.

Ryan also checked the work in person and verbally approved it. This provided an additional peer review of the group's work.

### What I learned

This stage improved my understanding of release preparation and software testing.

I learned that a successful implementation is not the only requirement for a software release. Documentation, testing, version control, reproducibility and submission-package verification are also important.

I also developed a better understanding of how the different SmartCare modules work together and how automated tests can provide evidence that the system's functionality is behaving as intended.

### AI assistance reflection

AI assistance was used to help identify isseus.

The use of AI was treated as supporting assistance rather than a replacement for testing or understanding the application. The final evidence was based on the repository, observed test results and the actual application demonstration.

### Handover

The SmartCare UG release candidate contains the implemented patient, practitioner and appointment functionality, together with appointment filtering and sorting.

The recorded final tested commit is:

9b10a5d4f75cdb45a10464cc5d224ea5739ae7f9

The full regression suite reported 52 passing tests.

The main known limitations are the use of in-memory storage, the console-based interface and the absence of production-level authentication and external integrations.

The remaining handover tasks are to verify the final repository state, create the final source ZIP and test the extracted package.

**Final handover status:** Release candidate reviewed and peer-approved in person; final submission-package verification remains outstanding.
