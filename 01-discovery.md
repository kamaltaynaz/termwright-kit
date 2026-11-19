# 01. Discovery: interview me before you write anything

*Paste this after `00-ground-rules.md` has been accepted.*

---

You are going to help me build a tool that prepares a term's courses in Canvas. You know how Canvas works in general. You do **not** know how mine is set up, and a tool built on guesses will be wrong in ways that are expensive to find. So before you write any code, interview me.

## How to run the interview

- Ask in **rounds of at most six questions**, grouped by topic. Wait for my answers before the next round.
- Where you can find the answer yourself with a **read-only** Canvas call (once I give you a test environment and a token), do that and show me what you found rather than asking. Still ask me to confirm it.
- If I say "I don't know", write it down as an open question with an owner, and suggest how we could find out.
- Do not skip a topic because it seems obvious. Several of the most expensive mistakes in the tool this kit came from were things "everyone knew".
- Keep a file called `docs/ANSWERS.md` with every question, my answer, the date, and whether it is **confirmed**, **assumed** or **open**. Update it after every round.
- Never ask me to paste a token, password or API key into the chat. Ask me where it is stored and how it will be provided (see topic 4).
- When all topics are covered, summarise the answers in a page, list every assumption and open question, and **stop and wait** for me to confirm. Do not start `02-spec.md` until I say so.

## Topics and questions

### 1. My Canvas and how courses are organised
- Which Canvas environments exist for me (production, a test or beta copy, a sandbox)? Which may we write to? How often are they refreshed from production, and what happens to our test data when they are?
- How is the account tree arranged (a root account, sub-accounts, where do term courses live)? Is there an account where courses are created automatically from a student information system feed? Which accounts may this tool write to, and which must it never write to, even by accident?
- How are terms defined and identified? Do they already exist for the term we are building? Who creates terms?
- Is there a naming and ID convention for courses and sections (the human name and the SIS ID)? **Write the exact pattern down with an example.** Do other systems (a student enrolment feed, a reporting tool) depend on these IDs? What would go wrong, and for whom, if one were wrong?
- Does Canvas create anything automatically when a course is created or when someone is enrolled (a default section, a template copy, tools switched on)? Is that expected, or a nuisance?
- What time zone should new courses use, and what do they get by default?
- Which roles exist (including custom ones, such as a teaching-assistant role)? Which roles will this tool ever assign? Which must it never assign?
- Which Canvas features does my institution use or forbid (new quizzes, blueprint courses, outcomes, publishing rules)? Are courses ever published by this tool, or must a human do that?

### 2. Where the data comes from and where it goes
- What is the source of truth for "which courses exist this term" (a registrar spreadsheet, an SIS export, a database, a web page)? Show me a sample with names and IDs replaced.
- What are its quirks: leading zeros in course numbers, placeholders for unknown instructors, multiple instructors per row, sections that are not real sections, duplicate rows, encoding problems?
- Is there a second source (for example faculty forms about their needs, a textbook list, a copy-from-previous request)? How does it arrive and in what shape? May the tool read it automatically? Is it trustworthy, or could it contain mistakes or hostile text?
- Which courses should be built, and who decides? (Everything in the list, or only rows someone has marked?)
- Where should results go (Canvas only, a spreadsheet, a report, a chat message)? Who reads them?
- When two sections of a course exist, are they one shared Canvas course or separate ones? Who decides, and how (history, a rule, a person)? What must the tool do when nobody has decided?

### 3. What the tool should do, step by step
- Walk me through what you currently do by hand or by script each term, step by step, in order. For each step: what must be true before it, who approves it, how you check it worked.
- Which steps are **creating** (courses, sections), **people** (instructors, assistants), **content** (copying from an earlier course), and **tools** (textbook platforms and other integrations)? Which of these should be a separate phase with its own approval?
- For people: how do we find the right Canvas user from what the source gives us (login ID, email, SIS ID)? What must happen if there is no match or several? How should "no instructor yet" and "instructor said they won't use Canvas" be handled?
- For content copies: which earlier course is the source, who chooses it, and what must the source satisfy (same institution, taught by the same person)? Which content types should be copied and which must not (settings, syllabus, announcements, calendar events, tools, dates)? How should dates be handled? Should the copy be checked afterwards, and how?
- For tools: which integrations get switched on in a course, how are they identified, and is any of this decided per course (for example by textbook vendor)? Which are installed as tabs, which as module items?
- What should the tool never do on its own?
- What undo do you need? A full rollback of a run, a "safe undo" on production only, a list of what to fix by hand?

### 4. Access and authentication
- How will the tool authenticate to Canvas (personal access token, an OAuth app, a service account)? How long does a token live? Who creates it?
- What exact permissions does the account behind the token have in each environment? What is the least it needs for the first phase?
- Where will the token be kept (an environment variable, a file with restricted permissions outside the project, a secret manager)? How will it be rotated or revoked? Who is responsible after each run?
- May the tool read personal data (names, emails)? Where must that data never appear (logs, reports, chat messages, the repository)?

### 5. Triggers and frequency
- What starts a run: a person, a schedule, a file arriving, a form being submitted? How often per term? Is it a whole-term job only, or also small ad-hoc changes? (A tool built for whole-term runs can be much safer than one that tries to handle every one-off request; decide this deliberately.)
- What time limits matter (registration dates, term start)? What happens if a run fails halfway?

### 6. Notifications
- Who must be told what, and how (chat, email, a report file)? Must the tool avoid triggering any Canvas notifications or invitation emails? In which environments are real emails allowed?
- Who should be alerted when the tool itself breaks or goes silent?

### 7. Where it runs, and what it may be written in
- Where will it run (a laptop, a server, a cloud job)? What happens when that machine is asleep, offline or replaced?
- Which programming languages and libraries are allowed or banned by my institution? Is there an approval process for new dependencies?
- Is there a policy on storing logs, on retention, on where student or staff data may live?

### 8. Rate limits, scale and cost
- Roughly how many courses, sections and people per term? How many term runs per year?
- Do my environments throttle API requests? Are test environments slower or stricter than production? (Offer to measure with a few read-only calls.)
- What is my budget for AI agent usage, and should the build be paced to stay inside it?

### 9. Edge cases and "done"
- Tell me about the last time something went wrong with a term set-up. What happened and who noticed? What should the tool do so that never happens again?
- Which weird cases do you know about (one instructor teaching every section, a course that exists only on a form, a section that was renamed late, a course that lost its schedule)?
- What does "done" look like for a first working version? For the whole term? Who signs off?
- What is **out of scope** for now?

## What you produce

1. `docs/ANSWERS.md` as described above.
2. A one-page summary: what you understood, the five riskiest assumptions, and the open questions with owners.
3. A short list of anything in my answers that conflicts with the ground rules in `00-ground-rules.md`.

Then **stop and wait**. Do not write a spec, code or a plan until I have confirmed the summary.
