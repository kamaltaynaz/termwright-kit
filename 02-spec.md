# 02. Spec: write it down before you build

*Paste this after I have confirmed the discovery summary.*

---

Turn `docs/ANSWERS.md` into a written specification. Nothing gets built until I have read it and said it is right. A spec that lives only in your head disappears at the end of the session; a spec in a file survives it and can be reviewed.

## Rules for writing the spec

- Everything in it must trace to an answer in `docs/ANSWERS.md`, a ground rule, or a decision you propose and I approve. Mark which.
- Where my answers leave a choice open, **do not choose silently**. Put it in the open-questions list with a recommended default and the reason.
- Write in plain sentences. Short. A new person should be able to read it and understand what will happen to a course.
- Do not put code in the spec. Describe behaviour and give examples with placeholder values.

## Produce `docs/SPEC.md` with these sections

1. **Purpose and scope.** What the tool does, for whom, how often. What is out of scope, with the reason.
2. **Environments.** Each Canvas environment, what the tool may do in each, and how it knows which one it is talking to. State how it prevents a plan made for one environment from being applied to another.
3. **Inputs.** Each input, its shape, its quirks and how each quirk is handled. Include a small invented sample.
4. **Phases.** For each phase (for example: create courses and sections; copy content; enrol people; switch on tools), list what it reads, what it writes, what must be true before it starts, what it must never do, and how it is verified. Say why the phases are in this order.
5. **Write operations.** The complete, closed list of kinds of write the tool may perform, each addressing a Canvas object by a stable ID, each safe to repeat. Anything not on the list is forbidden.
6. **The plan, approve, apply, verify cycle.** What a plan contains, how it is bound to the data it was made from, how approval works, what the dry run shows, what is checked afterwards, how stale plans are refused, and how a run that stopped halfway is resumed.
7. **Safety limits.** Batch sizes, caps per plan, pacing between writes, a circuit breaker that stops after repeated failures or an authorisation error, and a lock so two runs cannot overlap.
8. **Naming and IDs.** The exact patterns, with examples, and the checks that enforce them.
9. **People.** How users are found, what happens with no match or several, which roles are assigned, which are never assigned, and what happens with notifications in each environment.
10. **Content copy rules.** What is copied, what is not, how dates are treated, who chooses the source, what a source must satisfy, how a finished copy is checked.
11. **Tools and integrations.** How each is identified in Canvas, how it is switched on, and what the tool does when the expected one is missing.
12. **Undo.** What can be undone automatically, what only on test environments, what is left as a manual list. Say what undo will never touch.
13. **Secrets and personal data.** Where each lives, who can read it, and what is forbidden in logs and reports.
14. **Reporting and alerts.** What is reported, to whom, with what content. What is never included.
15. **Operations.** How it is scheduled, how failure and silence are noticed. (See `07-operate.md`.)
16. **Decisions log.** Each decision: date, what, why, who. Seed it with everything already decided.
17. **Open questions.** Each with an owner, a recommended default, and what is blocked until it is answered.
18. **Acceptance criteria.** A numbered list of checks, each one something that can be run or observed and that has a clear pass or fail. For example: "A plan applied twice makes no changes the second time", "No request is ever sent to a root account for writes", "An expired token is refused before any call", "A course with an unmatched instructor is held, not guessed".
19. **Risks.** Mass or wrong enrolment, wrong term, duplicate courses, stale plans, concurrent runs, rate-limit storms, partial runs, secret leakage, an agent approving its own plan. For each, the control.

## Then

1. Show me a one-page summary of the spec and the list of open questions.
2. Run your own check: for each acceptance criterion, name the test level (`04-test.md`) that will prove it. Flag any criterion you cannot test.
3. **Stop and wait.** I will read `docs/SPEC.md`, answer open questions and approve it. Record the approval in the decisions log with the date. Do not start `03-build.md` until I tell you to.
