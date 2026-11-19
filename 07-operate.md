# 07. Operate: keeping it running, and noticing when it does not

*Paste this when the first real run is finished. A tool that runs only a few times a year, or that watches something daily, has a particular problem: it can fail silently for weeks. This prompt is about making sure someone finds out.*

---

Write `docs/OPERATIONS.md` and set up what it describes. Ask me before installing anything that runs automatically.

## 1. What runs, and when

For each job (a daily watch, a form check, a term build), write down: what it does, what triggers it, how often, how long it should take, what it reads and writes, which credentials it needs, where its output goes.

- Prefer **whole-job runs with a time box** over always-on processes. Short-lived credentials created for a run and deleted after it are safer than a standing one.
- Anything that runs unattended is **read-only** unless I have explicitly approved otherwise. Writes always go through plan, approval and apply.
- If the job runs on a laptop, say what happens when the laptop is asleep, closed or off, and whether missed runs are made up. If that is not acceptable, propose a different home for it.

## 2. Scheduling

- Show me the scheduler configuration (a launch agent, cron entry or cloud scheduler) as text **before** installing it. Install only on my yes.
- Make the install script do nothing but print by default, with a flag to actually install.
- A scheduled job runs in a restricted environment. **Test it by running it the way the scheduler will**, not just by hand, and check the log afterwards. Common surprises: it cannot read a folder your user account can; it has a different path and cannot find the interpreter; it needs a permission that was granted to your terminal but not to the scheduler.

## 3. Logs

- Every run writes a log line with start time, end time, result and counts. Rotate logs so they do not grow forever.
- Logs and reports never contain tokens, email addresses or names. Test that.
- Keep an audit log of every write: when, which environment, which action, which target, what was there before, what is there after. This is what makes undo and incident review possible.

## 4. Alerts

- Decide with me who is alerted about what, and how (chat, email, a file I check). Use the least personal channel that works. Alerts carry counts and course numbers, not people.
- Alert on **failure** (a job exited with an error, a source could not be read, the credentials were refused) and on **changes worth acting on** (a new course appeared, a section was removed).
- A failure to read the source must be reported as a failure, **never as "everything was removed"**. Keep the last good snapshot.
- A missing alert destination should warn loudly, not fail quietly.

## 5. A heartbeat

A silent tool looks exactly like a working tool that has nothing to report. So:

- Each job writes a **heartbeat** at the end of every run, success or not: a timestamp in a known place.
- A second, independent check (a different scheduler, a person's calendar reminder, an uptime service) looks at the heartbeat and alerts if it is older than expected. Set the threshold from the job's schedule plus slack.
- Include a **weekly "still alive" message** if nothing else has been sent.
- Test it: stop the job on purpose and confirm someone is told.

## 6. Handling failures

For each job, write a short runbook entry:

| Situation | What the tool does | What a person does |
|---|---|---|
| Credentials expired or refused | Refuse to run; alert | Create new credentials; run the preflight check |
| Source site or file unavailable or malformed | Report failure; keep last good data | Check the source; re-run |
| Rate limit hit | Back off, stop at the cap, report partial | Wait; re-run (it continues from cache) |
| Run stopped halfway | Safe to run again; no duplicates | Re-run the same plan |
| A plan was applied that should not have been | Nothing automatic | Use the undo path; follow `06-rollout.md` "When something goes wrong" |
| Unexpected data (a new kind of row, a new form question) | Hold it; report; do not guess | Decide; update the rules; add a test |

## 7. Credentials

- Tokens are created for a run, used, and then **deleted and revoked in Canvas** by me. Remind me at the end of every session.
- The tool checks expiry before any call and warns when little time is left.
- Keep a list of every credential that exists, where it lives and when it expires. Tell me about stale ones.

## 8. Change management

- Every change to the tool goes through the same cycle: spec or decision log entry, tests, review for anything that writes, commit.
- Keep the spec and the code in step. If a decision in the log is not reflected in the spec, say so.
- Before each new term, re-run the discovery questions that could have changed (accounts, roles, naming, vendors, form fields) and update `docs/ANSWERS.md`.

## 9. At the end of each term

Write a short retrospective: what ran, what broke, what was fixed by hand, what should become a rule or a test, what to ask differently next time. Add it to the decisions log.

Then show me `docs/OPERATIONS.md`, what you installed (if anything), and the results of the failure and heartbeat tests. **Stop and wait.**
