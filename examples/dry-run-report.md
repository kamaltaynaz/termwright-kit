# EXAMPLE ONLY: plan summary and dry-run report

```
ENV PRODUCTION (https://canvas.example.edu) | term TERM_ID | batch 1/3 | observed 2 min ago
input: courses.csv, sha256 ..., 10 of 160 rows planned
kinds: create_course 10, create_section 14
courses: 10 (10 new, 0 existing)
BANNERS: none           <- banners for OVERRIDE, RETRY, RESET or TEST would appear here

Actions
  1. [create_course]  create TERM-12345-A   (row 4)
  2. [create_section] create section 12345-A-... in TERM-12345-A
  ...
Held rows (not in this plan, need a decision):
  - 12345: two sections, no decision on shared or separate
```

Dry run:

```
==> DRY RUN against PRODUCTION: 24 steps (plan PLAN_ID). Nothing is written.
  would create_course  TERM-12345-A
  ...
==> 24 would change, 0 already done
To apply: run the apply command with --apply (you will be asked to approve the plan first).
```
