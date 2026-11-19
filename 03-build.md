# 03. Build: small steps, each tested

*Paste this after I have approved the spec.*

---

You will now build the tool described in `docs/SPEC.md`. The ground rules in `00-ground-rules.md` still apply to everything below.

## How to work

1. **Plan the build first.** Break the spec into milestones, each small enough to review in one sitting and each ending in something runnable. Write them to `docs/PLAN.md` with the acceptance criteria each one satisfies. Show me the plan and wait for my go-ahead.
2. **Start with the foundations, in this order**, unless my spec says otherwise:
   1. Project scaffold, configuration, the place secrets are read from (outside the repository), an audit log, a way to run tests, a linter.
   2. A thin, read-only Canvas client: authentication, pagination, rate-limit handling, retries with back-off, a request cap per run. No write calls yet.
   3. Pure logic that needs no Canvas at all: parsing the input, building IDs, matching people. These are the easiest to test thoroughly.
   4. A stand-in for Canvas (see `04-test.md`) with the quirks you learned in discovery.
   5. The plan and apply machinery: a plan file, approval, a dry run, guards for age, environment and overlapping runs.
   6. One kind of write at a time, each with "before, execute, verify", each safe to repeat. Start with the least dangerous.
   7. The phases, in the order from the spec.
   8. Reports and alerts.
   9. Undo, only after the above are solid.
3. **For every milestone:** write the tests first or alongside; run the full test suite and the linter; update the docs; commit with a clear message. One idea per commit. **Do not commit or push unless I have said you may.** Show me what changed.
4. **Review your own work before showing me.** Re-read the diff. Look for the things that go wrong in tools like this: a request that could hit the wrong environment, a write without a read-before, a log line that could contain a secret or an email address, a loop with no cap, an error that is swallowed, an assumption not in the spec.
5. **Keep records.** Every decision goes in the decisions log. Every assumption you had to make is marked and reported to me. Keep a file index so a new session can find things.
6. **When the spec is wrong or silent,** stop and ask. Do not quietly fill the gap. If you find a mistake in the spec, say so and propose the change; I approve it and you record it.
7. **Pace yourself.** Use a smaller, cheaper model for mechanical work (renames, boilerplate, running tests). Use your best model for anything that writes to Canvas, enforces a safety rule, or parses untrusted input. If you hand work to helper agents, give each a narrow task, run one at a time against any throttled environment, and read their diffs yourself. A helper's summary is not evidence.
8. **Never build around a safety rule.** If a safety rule is getting in the way of a test, change the test, not the rule. If you think a rule is wrong, tell me.

## Design habits that will save you

- **Address Canvas objects by their stable IDs (such as the SIS ID), and resolve internal IDs at the moment of writing.** A plan made before a course exists must stay valid after it is created.
- **Treat Canvas as the truth and your own saved state as a cache.** Re-read before you write.
- **One kind of write per Canvas concept.** No generic "write anything" function.
- **Write only what is missing.** A second run of the same plan must do nothing.
- **Do not retry a write blindly after a network error.** Read the state back first; if you still cannot tell, report that the result is unconfirmed and stop.
- **Make the first version refuse rather than guess.** A held row is better than a wrong course.
- **Things that people edit by hand afterwards (a course's settings, a tab someone hid) should be applied once and then reported as drift, not overwritten every run.** Things that must stay exact (IDs, the course and section structure, who is enrolled) should be checked every run.
- **Keep the plan readable.** A summary first (counts, environment, anything unusual), then the list of actions. People approve what they can understand.

## When a milestone is done, report

- What you built and which acceptance criteria it now meets.
- Test results (counts, not just "all passing"), lint result.
- What you did **not** do or could not check.
- Any assumption or open question that came up.
- The next milestone.

Then wait for my go-ahead.
