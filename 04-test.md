# 04. Test: four levels, and the faults to simulate

*Paste this when you start building, and again before each stage of testing. Apply it to every milestone.*

---

A tool that writes to Canvas has to be tested in stages, because each stage catches a different kind of mistake and nothing replaces the next one. Follow these levels in order. Do not skip one because a later one "would catch it".

## Level 1: unit tests

Pure logic with no network: parsing input rows, building and checking IDs, matching people to users, comparing plans, computing diffs, reading configuration, handling tokens and expiry.

- Include the awkward inputs from discovery as test cases: leading zeros in course numbers, blank and placeholder names, duplicate rows, multiple people in one cell, non-ASCII characters, an email where a login ID was expected.
- Add a **golden file test** for any transformation that produces a file someone will rely on: it must match a known good output exactly.
- Keep these fast. They run on every commit.

## Level 2: a stand-in for Canvas

Write a **stateful fake of the Canvas API** that behaves like the real thing in the ways that matter to you, and use it to test everything that writes.

- It must remember what was created, so "create twice" and "enrol twice" behave as in Canvas.
- Give it the quirks you found in discovery and in Canvas's documentation. Examples of quirks to model, if they apply to your Canvas: some endpoints ignore a JSON body and need form encoding; a newly created object comes back without a field you asked for; creating something may trigger an automatic copy or an automatic default section; deleted objects keep their IDs reserved for a while; a status field is reported differently for an old object than a new one; a list endpoint returns a partial page.
- Give it **fault injection**: make any call fail with a server error, a timeout, an authorisation error, a rate-limit response, or a malformed page, on demand.

Use it to test:
- A plan applied twice does nothing the second time.
- A run interrupted halfway and resumed produces the same end state as an uninterrupted run.
- After a server error on a write, the tool reads back and reports "unconfirmed" if it cannot tell, and does not blindly retry.
- After repeated failures or an authorisation error, the circuit breaker opens and nothing else is written.
- A stale plan, a plan for another environment, and two overlapping runs are all refused.
- The allowlist: any write not on it is refused.
- The "never" rules: never a write to a forbidden account, never an unenrol outside the undo path, never a notification outside production.
- Undo: it removes exactly what the run created, and leaves alone anything changed since.

## Level 3: your Canvas test or beta environment

Run a human-supervised rehearsal against a real, non-production Canvas.

- Create a **throwaway namespace** (a course ID prefix you will recognise) so everything the rehearsal creates can be found and removed.
- Use a few hand-picked courses first, including at least: a normal course, a multi-section course, a course with several instructors, a course with no instructor, and one with a copy source.
- Run the whole cycle: plan, approval, dry run, apply, verify, then re-plan and confirm there is nothing left to do.
- Rehearse **undo** here, including one that is interrupted halfway and resumed.
- Measure request counts, speed and rate-limit behaviour, and write them down. Test environments are often throttled much harder than production, so find out.
- Do not enrol real people here unless you have proved that no email can go out. Prefer enrolling only the tester.
- Record **what this level caught that levels 1 and 2 did not**. That list is the evidence of why levels exist.

## Level 4: production, in the smallest possible pieces

This is not a test level in the usual sense; it is the first real use. Follow `06-rollout.md`.

## Faults to simulate

These are the kinds of faults that turned up in real use of a tool like this. Make sure each one has a test or a rehearsal.

| Fault | What should happen |
|---|---|
| A multi-section course is planned as a single shared course by default | The tool refuses to guess. It asks, or holds the row. Test the "nobody has decided" case. |
| One instructor teaches every section of a course that history says to split | The tool flags it instead of creating empty separate courses |
| A copy source belongs to the wrong part of the institution, or the source's instructor is not a real teacher there | The copy is refused. A different check (for example a missing teacher) can be overridden deliberately; the institution check cannot |
| The token is expired, revoked early (while a stale expiry record says there is time) or has the wrong permissions | The preflight check refuses before any other call |
| A configuration file contains a placeholder where a value should be | It is detected and refused, not read as a date in the past |
| New courses come out with the wrong time zone, or a copy overwrites it | A check catches it and a repair step fixes only that setting |
| A tool link opens in a new tab when it should open in the same one | The setting is explicit and verified |
| A problem with copying blocks everything else for that course | Only the copy is blocked; the other work for the course continues |
| An input field holds an email where a login was expected | It is normalised and logged, not silently dropped |
| A second planner run creates a duplicate plan | Duplicates are detected and refused |
| A copy finishes "successfully" but with fewer items than the source | The comparison reports it; the tool does not mark it done |
| An undo is interrupted halfway | Re-running it finishes the job and does not repeat the first half |
| A list read returns a partial page | The tool does not draw conclusions from a partial list |
| A log, report or chat message contains an email address, a name or a token | A test scans outputs for those and fails |
| The tool is asked to do an ad-hoc one-off outside its scope | It declines and says what to do instead |

## Report

For each stage you complete, give me: the number of tests (and how many are parameterised cases), pass, fail and skip counts, how long they take, the lint result, and a short list of **what this stage caught**. Do not claim a level is done until it has caught or failed to catch something real; "nothing found" is a result and must be reported as one. Then wait.
