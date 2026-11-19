# Canvas term builder: a prompt kit

A set of prompts that let an AI coding agent build, test and roll out **your own** tool for setting up a term's courses in Canvas (Instructure's learning management system).

This kit contains **no code from the tool it came from**. That tool was written around one university's Canvas set-up (its accounts, its course and section naming, its roles, its vendors, its forms), so it would not work anywhere else. What does carry over is the process the original followed: a written spec first, ground rules before any code, staged tests, and a rollout in small approved steps with a person reading every plan. The original lacked an independent review of its code, and this kit asks for one. The prompts here make an agent follow that process for your set-up.

## The problem this kind of tool solves

Before each term, someone has to turn a course list into Canvas: create the courses and sections with correct IDs, enrol the right instructors, copy last term's content, switch on the right tools (textbook platforms and similar), and keep checking afterwards. Done by hand it is slow, error-prone and repeated every term. Done by a script, it is fast until the script quietly does something wrong to hundreds of courses at once.

The kit is built around the second worry. The tool it produces should plan every write first, show you the plan, wait for your approval, apply it in small batches, and be able to say exactly what it did.

## Who this is for

- A Canvas administrator or learning-technology person who can describe how their Canvas is set up and can approve changes.
- Someone with an AI coding agent (for example Claude Code from Anthropic, or Codex, OpenAI's command-line coding agent) and basic comfort with a terminal.
- You do **not** need to be a programmer, but you must be willing to read plans and answer questions. The agent will ask a lot of them.

Many institutions already have this automated, with middleware and developers. Many more do not, and plenty of Canvas administrators still build each term by hand. The kit is for them. It is not tied to a Mac or to Python: your agent builds the tool in whatever fits your systems. That is also why this is prompts and not code. A script carries the assumptions of the place it was written; prompts carry the questions that surface yours, and the ground rules that keep the result safe.

## What you need before you start

1. **An AI coding agent** that can read and write files in a project folder and run commands.
2. **A Canvas test or beta environment** you may write to. Do not start on production.
3. **A Canvas API token** with the least permission that works, for the test environment first. Keep it out of the project folder.
4. **The input data your term starts from**: for example a registrar course list as a spreadsheet, or an export from your student information system.
5. **Permission** from whoever owns your Canvas to create courses and enrol people through the API.
6. A place to keep notes: the agent will write a spec, a decisions log and a test log as files in the project.

## How to use the kit

Work through the files in order. Each one is a prompt you paste to the agent; each tells the agent when to stop and wait for you.

| Step | File | What happens | You approve |
|---|---|---|---|
| 0 | `00-ground-rules.md` | The agent loads the rules for the whole build | Read them; add your own |
| 1 | `01-discovery.md` | The agent interviews you and writes down your answers | The answers file |
| 2 | `02-spec.md` | The agent turns the answers into a spec | The spec |
| 3 | `03-build.md` | The agent builds in small tested steps | Each milestone |
| 4 | `04-test.md` | Tests at four levels, ending in your test environment | The test report |
| 5 | `05-review.md` | An independent reviewer (a second agent or a person) checks the work | Each round's fixes |
| 6 | `06-rollout.md` | Read-only, then dry run, then one small piece live, then the rest | Every step |
| 7 | `07-operate.md` | Scheduling, alerts, a heartbeat, failure handling | The runbook |

`examples/` holds short, generic illustrations (an API call with paging, a config file, a dry-run report, a test stub). They are examples of shape, not a working tool.

Paste the ground rules first and keep them in the agent's instructions file (for Claude Code that is `CLAUDE.md`; for other agents, their equivalent) so they apply to every later step.

## Time and cost

- The original tool reached its first full run in roughly three days of intensive work, with refinements over the following week. A narrower tool (for example only creating courses, or only enrolling instructors) will be much quicker. Your time will go mostly on answering questions and approving plans, not on typing.
- Expect heavy use of your AI agent's usage allowance. The notes from the original build record using most of a plan's usage in about a day, which is why the kit tells the agent to use cheaper models for mechanical work and to run one task at a time.
- Test environments in Canvas are often rate limited far below production. Budget time for that.

## Honest limits

- **This is not a product.** It is a method and a set of prompts. The agent writes your tool; you own it, and you are responsible for what it does.
- **The agent will make mistakes.** The kit is designed so that mistakes are found in tests, plans and reviews rather than in production, but it cannot guarantee that.
- **Your Canvas is different from ours.** Many of the questions in `01-discovery.md` come from places where the original tool depended on one institution's set-up. Expect more that we did not think of.
- **Reviews are only as independent as you make them.** A second agent that reads the first agent's summary is not independent. `05-review.md` tells the reviewer to distrust the documents and read the code, and you should make sure it does.
- **Some things were never tested live in the original**, such as notification behaviour on production and some rate-limit storms. The kit tells the agent to treat such behaviour as unknown until proven.
- **Third-party platforms change** (textbook platforms, LTI tools, Canvas itself). Ask the agent to check current documentation and to mark anything it could not verify.
- No warranty. See `LICENSE`.

## Credit

The credit belongs to the process: a written spec before code, ground rules with reasons, staged testing and an approval-gated rollout. The original had no independent review, and its first production mistake was caught by a person reading a plan, not by a reviewer. `05-review.md` is what this kit asks for and the original lacked: it is written from principles, not from review rounds that were run on the original. The prompts are original text written for this kit.

## License

MIT. See `LICENSE`.
