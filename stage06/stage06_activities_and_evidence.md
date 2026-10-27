# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [response]
- Members, GitHub usernames and cohorts: [u3323819 (Deng), u3334274 (Seb), u..]
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
| [https://github.com/ShadowMonrch/st1-assignment-3/issues/2#issue-6063281832] | [FR-02 Patient Search by ID] | [Deng] | [Correct stored patient returned; whitespace handled; invalid IDs raise ValueError; missing IDs raise LookupError; case-sensitive IDs; tests pass] | [PR open; review pending] |
| [---]|[---]|[---]|[---]|[---]|

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [Deng (u3323819)]

- Implementation:  
[Implemented PatientService.find_patient() in project/smartcare/services.py. The method trims whitespace, returns the stored patient object, raises ValueError for blank or invalid IDs, and raises LookupError when a patient does not exist]

- Testing:  
[Created project/tests/test_patient_lookup.py with five tests covering stored-object identity, whitespace handling, missing IDs, blank IDs and case sensitivity. Ran python -m pytest from the project/ directory and observed 13 passing tests]

- Review:  
[Submitted the feature/patient-lookup branch for review through a pull request. Independent review and approval are pending]

- Issue refinement:  
[Created the FR-02 Patient Search issue with a requirement, acceptance criteria, scope and Definition of Done]

- Design and responsibility discussion:  
[Kept the patient lookup implementation and its tests focused on FR-02]

- Debugging or integration:  
[Installed the development dependencies and resolved the test discovery/import-path issue by running pytest from the correct project directory. Integrated review and merge verification are still pending]

- Documentation or team support:  
[Recorded the contribution in this draft. Update the shared Stage 6 evidence file when the corresponding entries are verified]

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

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
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
