# 06. Rollout: from read-only to live, one proven step at a time

*Paste this when the tests and reviews are done. Every step needs my approval, and the approval for one step is not approval for the next.*

---

You are about to run the tool for real. This is where mistakes reach people. The rule for this whole file: **small, reversible, proven, then bigger.** Never make a step bigger than the last one you proved.

## Before any step

Confirm each of these out loud and tell me the answer. If any is "no", stop.

1. The test suite and linter pass, and you tell me the counts.
2. The last review round found no critical or high findings, or I have explicitly accepted the remaining ones in writing.
3. The token for this step is the right one for the right environment, is short-lived, has only the permissions it needs, and the preflight check passes (not expired, can read its own user record). **Never print the token.**
4. I know what step we are on, what it will change, and how to undo it.
5. Notifications: you can show me, from the code, that no email or notification can go out in this environment (or, in production, exactly which step will be the first to send one and that I have agreed).
6. There is a place to record what happens (the audit log and a short rollout log with date, time, step, plan identifier and result).

## The steps

### Step 0: read-only discovery on production
Run only read commands. Confirm that what the tool believes about production (accounts, terms, roles, existing courses, rate limits) matches reality. Fix the tool or the spec if it does not. **Write nothing.**
*Proof:* the request log shows only reads; the tool's picture of production matches what I see in Canvas.

### Step 1: plan only
Generate plans for the whole job. Planning must use only read requests. Show me the summaries and read me anything unusual. **Do not apply.**
- I (not you) read at least one plan in full, and a sample of the rest.
- **Ask me the questions the plans raise** before applying anything: which courses are shared and which separate, who is held, which sources are used. Wrong guesses here are the most expensive mistakes.
*Proof:* I have read the plans and answered each question; the answers are recorded.

### Step 2: dry run
Run the apply step without writing. It should say exactly what it would do. Compare with the plan.
*Proof:* dry run output matches the plan and my expectations.

### Step 3: one small piece live
Choose the smallest meaningful unit: one course, or one enrolment I pick myself. I approve it by the deliberate action at the terminal. You apply it. Then:
- Verify in Canvas yourself with a read request, and tell me what you see.
- Ask me to look at it in Canvas too.
- Re-run the plan: it must now say there is nothing left to do for that unit.
- If an email or notification could have been sent, **we find out now**, with this one case, before sending to everyone. Ask me to ask the one affected person; do not assume.
- Practise **undo** on it if it is safe to.
*Proof:* the unit exists as planned, the re-plan is empty, and I am satisfied.

### Step 4: a small batch
Ten or fewer units. Same cycle: approve, apply, verify with reads, re-plan.
*Proof:* as above, plus the request log shows no unexpected errors or throttling.

### Step 5: the rest, in batches
Keep the batches small enough that I can read each plan. After each batch, verify and re-plan. Stop at the first surprise. A **surprise** is anything the plan did not say: a different count, an error, a slow response, a course I did not expect.
*Proof:* after the last batch, a full re-plan for the term says there is nothing left to do, and a reconciliation (what the input says versus what Canvas has) matches.

### Step 6: phases in order
If the tool has phases (create, then copy, then enrol, then switch on tools), do each in order across the whole term, with steps 1 to 5 repeated per phase if the risk is different. Enrol people only after the content they might otherwise change has landed.

## When something goes wrong

1. **Stop.** Do not apply anything else.
2. Tell me what happened in plain words: what ran, what the result was, what you think went wrong, what you do not know.
3. Do not fix it by hand in Canvas without telling me. Do not run undo without telling me what it will do.
4. Propose the undo plan (from the tool's undo path) and the fix. Wait for my approval of each.
5. Write the incident in the decisions log: time, what, how found, what changed. Add a test that would have caught it.

Real runs of a tool like this found a wrong default only when the first production plan was read by a person who knew the courses. Reading the plan is not a formality.

## After each working session

- Remind me to delete or revoke any short-lived token.
- Update the rollout log with counts of what changed.
- Update any tracker we use (a spreadsheet, a status file) from the tool's own status output, not from memory.

## When rollout is finished

Produce a short report: what was built, counts of what changed, anything left to do by hand, problems and how they were resolved, things still unverified. Mark unverified things plainly. Then move to `07-operate.md`.
