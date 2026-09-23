---
name: masterclass-build
description: Turn a participant's own work problem into a bounded, testable workshop prototype with a local fallback and practical handover.
---

# Bring your own problem

Translate the participant's problem into one demonstrable workflow: a person supplies an input, the tool performs a useful action, and the person receives a result they can check. Use `data/problem-brief.md` if no work example is available. Do not let an absent connector block the local workflow.

Establish the minimum missing details: intended user, current task, sample input, desired output, what a correct answer looks like and which outside systems are essential. Infer routine choices from the request and record them; ask only for decisions that materially change the result or authorization.

Write a short build brief with a primary use case, a small success criterion, data boundaries and a stretch goal. Pick one thin end-to-end slice before adding multi-agent architecture, vector stores or background jobs. Prefer an existing runtime and a local file/SQLite adapter unless the requested behavior needs more infrastructure.

Use a local fixture adapter for unavailable email, CRM, calendar, search or payment services. Name simulated responses honestly. Keep the integration interface clear so a real connector can replace the fixture later. Do not create provider accounts, purchase credits or send real messages just to complete a demo.

Build the working slice, then test a realistic input, a missing/invalid input and a second run. For stateful workflows, demonstrate what repeats and what is deduplicated. For model outputs, preserve the evidence or transformation record needed to review the answer and show uncertainty. Add one relevant specialized masterclass skill only when it helps the task.

Finish with a browser/terminal demonstration and a handover containing startup commands, inputs, outputs, known limits, actual verification and the next improvement. If deployment is requested, use the separate deployment skill and assigned sandbox. Minimum outcome: a repeatable local prototype solving one part of the participant's stated problem, with no undisclosed simulated capability.
