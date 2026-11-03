# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [Group 5]
- Members, GitHub usernames and cohorts: [u3323819 (Deng), u3334274 (Seb), u3324852 (Ryan)]
- Repository URL: [response]
- Starting SHA: [response]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: [FR-02 — Patient Search by ID]
- Context: [SmartCare needs a reliable way for staff to find registered patients using their patient IDs]
- Requirement: [Implement patient lookup through PatientService.find_patient() according to the Stage 6 service contract]
- Acceptance criteria: 
[A valid patient ID returns the correct stored Patient object.
Leading and trailing whitespace is handled correctly.
Blank or invalid IDs raise ValueError.
A valid-format ID that does not exist raises LookupError.
Patient IDs remain case-sensitive.
Automated tests cover successful lookup and relevant error cases.
Existing tests and functionality continue to work.]

- Scope: [Implement patient lookup in the existing service layer and add focused automated tests. Avoid unrelated changes]
- Definition of Done: 
[The implementation follows the existing service contract.
Relevant automated tests pass.
Changes are committed and pushed to the feature branch.
A pull request is reviewed by another group member before merging.]

- Owner: [Deng (u3323819)]
- Actual issue link: [(https://github.com/ShadowMonrch/st1-assignment-3/issues/2#issue-6063281832)]

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: [FR-06/FR-07 — Appointment Cancellation and Retained History]
- Context: [SmartCare needs to support appointment cancellation while preserving appointment records for historical reference]
- Requirement: [Implement appointment cancellation through the existing service layer and retain cancelled appointments in the system's history]
- Acceptance criteria: 
[A valid appointment can be cancelled using its appointment ID.
Invalid or unknown appointment IDs are handled appropriately.
Cancelled appointments retain their history rather than being deleted.
Appropriate tests verify successful cancellation and error cases.
Existing functionality and tests continue to work.]

- Scope: [Implement appointment cancellation and retained-history behaviour using the existing domain and data-store design. Avoid unrelated refactoring]
- Definition of Done: 
[The implementation follows the agreed service contract.
Relevant automated tests pass.
Changes are committed and pushed on the feature branch.
Another group member reviews the pull request before merging.]

- Owner: [Seb (u3334274)]
- Actual issue link: [https://github.com/ShadowMonrch/st1-assignment-3/issues/1#issue-6058149745]

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | [Weak] | [It doesn't explain what changes or why] |
| final version | [Weak] | [It doesn't identify the actual improvement and may be reused for multiple commits] |
| Add patient search by ID | [Strong] | [It clearly describes the feature being added] |
| fix stuff | [Weak] | [It is vague and doesn't communicate the problem fixed] |
| Prevent cancellation of completed appointments | [Strong] | [It describes a specific behaviour and the rule being enforced] |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns:
[The PR includes unrelated patient-field renaming, code restructuring and a new dependency. These changes go beyond the appointment cancellation requirement and make the PR harder to review]

- Responsibility and architecture concerns:
[Unrelated changes increase the risk of breaking existing functionality and make it harder to identify who is responsible for each change. They may also introduce unnecessary architectural complexity]

- Testing and review concerns:
[The reviewer must inspect and test more code than necessary. Unrelated changes need their own justification and tests, and the new dependency needs a clear reason]

- Changes to remove or separate, with reasons:
[Keep appointment cancellation and retained-history changes in the current PR. Move unrelated patient-field renaming and refactoring into separate issues and PRs if they are genuinely required. Remove the new dependency unless its necessity is demonstrated. This keeps the PR focused and easier to test and review]

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: 
[The review provides no specific code observations, requirement checks, test details, edge-case analysis or explanation of how the implementation satisfies the acceptance criteria]
- Follow-up review question 1: 
[Does the implementation satisfy every acceptance criterion in the linked issue?]
- Follow-up review question 2: 
[Does the code preserve the required appointment state transitions and reject invalid cancellation attempts?]
- Follow-up review question 3: 
[Does cancellation retain the appointment record and its history instead of deleting it?]
- Follow-up review question 4: 
[Do the tests cover successful cancellation, invalid transitions, missing appointment IDs and preservation of existing records?]
- Follow-up review question 5: 
[Does the PR contain unrelated changes, and have the relevant tests been run against the actual diff?]
- Additional questions if useful: 
[Are errors handled according to the service contract? Could any change break existing booking or lookup behaviour? Is there evidence that the integrated code passes the required tests?] 
[A reviewer must independently verify the implementation and evidence rather than accepting Copilot's conclusion without checking it]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [response] |
| Commit message convention | [response] |
| PR size | [response] |
| Another-member review requirement | [response] |
| Merge rule | [response] |
| Significant Copilot disclosure rule | [response] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
| [https://github.com/ShadowMonrch/st1-assignment-3/issues/1#issue-6058149745] | [FR-06/FR-07 Appointment Cancellation and Retained History] | [Seb] | [Valid cancellation; appropriate error handling; history retained; tests pass] | [In progress; verify current status] |
| [https://github.com/ShadowMonrch/st1-assignment-3/issues/2] | [FR-02 Patient Search by ID] | [Deng] | [Correct stored patient returned; whitespace handled; blank and non-string IDs raise ValueError; unknown IDs raise LookupError; IDs remain case-sensitive; tests pass] | [Merged into main via PR #3] |
| [---]|[---]|[---]|[---]|[---]|

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [https://github.com/ShadowMonrch/st1-assignment-3/pull/3 ,PR #3 — FR-02 Implement Patient Lookup]
Linked issue and requirement: [Issue #2 — FR-02 Patient Search by ID] 
- Feature branch: [feature/patient-lookup]  
- Changed behaviour: [Implemented patient lookup, returning the actual stored patient object, trimming whitespace, rejecting blank and non-string IDs with ValueError, raising LookupError for unknown valid IDs, and preserving case sensitivity]  
- Meaningful commits: [ec13233 — Implement patient lookup service; a6ae59c — Merge main into patient lookup feature; faa7f8a — Consolidate patient lookup tests into service tests; 84a33b9 — Validate patient lookup IDs]  
- Test command, directory and observed result: [python -m pytest, run from project/; 29 passed after merging into main]  
- Another-member reviewer: [Ryan (u3324852); GitHub shows one approving review]  
- Human observations recorded before Copilot: [Ryan said most of the implementation looked fine, but he suspected there might be a problem he could not pinpoint. Record the actual review discussion or link if available]  
- Requirement, responsibilities, test assertions and unrelated-scope checks: [Reviewed patient lookup behaviour against FR-02, including stored-object identity, whitespace, invalid IDs, unknown IDs, and case sensitivity]  
- Key feedback: [Copilot identified that non-string IDs could raise AttributeError instead of the required ValueError]  
- Author response/change and verification: [Added explicit type and blank-string validation before calling .strip(). Added a non-string ID test. The full suite passed with 29 tests]  
- Reviewer recheck and approval: [Ryan approved the updated changes on GitHub; the PR timeline records one approving review]  
- Merge outcome and SHA: [Merged into main; merge commit d576e06]  
- Significant Copilot assistance: [Used Copilot to review the implementation and tests; evaluated its non-string ID finding against the service contract, addressed the finding, and verified the result with tests]  
- Linked issue closure: [Check issue #2 and record its actual closed/open status]  
- Each member updated main: [Deng pulled origin/main and verified the integrated tests. Seb's and Ryan's confirmations are waiting] 
- Integrated verification after merge: [python -m pytest, from project/; 29 passed; code SHA d576e06]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [Deng (u3323819) — used GitHub Copilot to review the FR-02 Patient Search by ID implementation in project/smartcare/services.py and its associated tests]
- Prompt/purpose and relevant issue/diff: [Asked GitHub Copilot to review the patient lookup implementation and tests for correctness, acceptance-criteria coverage, potential defects, and missing test cases. The review related to https://github.com/ShadowMonrch/st1-assignment-3/issues/2 and https://github.com/ShadowMonrch/st1-assignment-3/pull/3]
- Summary of output: [Copilot found that non-string patient IDs could cause an AttributeError because .strip() was called before validating the input type. It recommended validating the input before trimming it and adding a test for non-string IDs. Copilot also mentioned redundant lookup logic in a pasted version of the method, but that redundancy was not present in the checked-in implementation reviewed]
- Human check against actual code, requirements and tests: [Compared the finding with the FR-02 service contract, which requires invalid IDs to raise ValueError, and inspected the actual implementation. Confirmed that the original method called .strip() before checking the input type, so the non-string input finding was relevant]
- Decision — Accept / Modify / Reject: [Accepted and addressed the non-string validation finding. The redundant-lookup observation was not applied because it did not match the checked-in implementation]
- Reason: [Explicit validation was needed to ensure non-string and blank IDs raise ValueError instead of allowing a non-string input to trigger AttributeError. The unrelated redundant-lookup observation did not require a code change]
- Verification/evidence: [Added explicit input validation in project/smartcare/services.py and added test_find_patient_non_string_id_raises_value_error in project/tests/test_services.py. Ran python -m pytest from the project/ directory and observed 29 passed. The changes were merged through PR #3, with merge commit d576e06]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [Ryan said that most of the implementation looked fine, but he suspected there might be a problem he could not pinpoint]
- Copilot noticed: [Copilot identified that passing a non-string patient ID could cause an AttributeError because the implementation called .strip() before validating the input type]
- Overlap: [Both reviews suggested that the implementation might have an issue, although Ryan did not identify the specific cause]
- What did the human reviewer notice that Copilot did not: [Ryan independently expressed concern that something might be wrong, but did not identify a specific defect]
- What did Copilot identify that the human reviewer initially missed: [Copilot identified the specific non-string input validation issue and explained why it could raise the wrong exception]
- Unsupported or incorrect Copilot suggestion: [Copilot also mentioned redundant lookup logic in a pasted version of the code. The checked-in implementation did not contain that redundancy, so that suggestion was not applicable to the reviewed version]
- Human judgement accepted, modified or rejected, and why: [The non-string validation finding was accepted and addressed. Explicit validation was added before .strip(), and a test was added to verify that a non-string patient ID raises ValueError. The redundant-lookup suggestion was not applied because it did not match the checked-in implementation]
- Which evidence justified merge approval: [The updated implementation and tests were reviewed, Ryan's approval was recorded on GitHub, and the integrated test suite passed with 29 tests after the pull request was merged]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [Deng (u3323819)]

- Implementation:  
[Implemented PatientService.find_patient() in project/smartcare/services.py, including whitespace trimming, stored-object return, and the required ValueError and LookupError behaviour]

- Testing:  
[Initially created five focused patient lookup tests, then consolidated the relevant tests into project/tests/test_services.py. Added a test for non-string IDs and verified that the full suite passed with 29 tests]

- Review:  
[Submitted PR #3 and received Ryan's recorded approval]

- Issue refinement:  
[Created the FR-02 Patient Search issue with a requirement, acceptance criteria, scope and Definition of Done]

- Design and responsibility discussion:  
[Kept the patient lookup implementation and its tests focused on FR-02]

- Debugging or integration:  
[Resolved a method-placement issue, corrected the implementation, merged the PR, pulled main, and verified the integrated suite]

- Documentation or team support:  
[Updated the Stage 6 evidence to reflect the final implementation, review, and integration results]

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[A high commit count does not necessarily demonstrate a strong contribution because commits can be small, repetitive, or poorly scoped. Strong contribution is better demonstrated by meaningful changes, reliable tests, clear commits, effective reviews, issue resolution and verified integration]

## L Stage 6 formative questions

1. What is version control?
[Version control tracks changes to files over time, allowing developers to review history, collaborate and recover earlier versions]

2. Why is a feature branch useful?
[A feature branch isolates a change from main, allowing development and testing without disrupting the shared stable branch]

3. What makes a commit a good engineering commit?
[A good commit is focused, understandable, appropriately sized and has a clear message explaining the change]

4. What is a pull request?
[A pull request proposes merging changes from one branch into another and provides a place for discussion, review and automated checks]

5. What is the purpose of code review?
[Code review checks correctness, requirements, maintainability, testing and potential risks before changes are merged]

6. What does a Git diff show?
[A Git diff displays differences between versions of files, including added, removed and modified lines]

7. What is a Definition of Done?
[A Definition of Done is an agreed set of conditions that must be satisfied before work is considered complete]

8. What is the appropriate role of GitHub Copilot in pull-request review?
[Copilot can help identify possible defects, risks and missing tests, but its suggestions must be checked against the requirements and actual code by a human reviewer]

9. Why should individual contribution not be judged only by commit count?
[Commit count doesn't measure the importance, quality or difficulty of work. Implementation, testing, reviewing, debugging and documentation can all provide meaningful contributions]

10. What is the Stage 6 engineering rule?
[Follow the required workflow: work on focused issues and feature branches, test changes, submit pull requests, obtain independent human review, use Copilot critically, resolve feedback and verify the integrated result before treating the work as complete]

## M Completion and handover

- Starting SHA: [Needs to be verified]
- Final Stage 6 code SHA: [d576e06]
- Test command: [python -m pytest]
- Working directory: [project/]
- Observed result: [29 passed in 0.09 seconds]
- PR and another-member reviewer: [(https://github.com/ShadowMonrch/st1-assignment-3/pull/3), Ryan (u3324852)]
- Unresolved issue or none: [Check the other two service targets and remaining team evidence before marking Stage 6 complete]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
