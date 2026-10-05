# Demo and handover

## Five-minute demo

| Time | Part | What to say or show |
| --- | --- | --- |
| 0:00–0:30 | The problem | Who has this task, how often, and how long it takes today. |
| 0:30–3:00 | Live run | Real or representative input goes in; the output comes out; show how you check it is right. |
| 3:00–4:00 | Where the agent failed | One thing it got wrong, how you noticed and what you changed. Take it from the PLAN.md table. |
| 4:00–5:00 | What next | What you would do on Monday and what would have to change for real use. |

## Before 17:00

- [ ] Start the tool from scratch with the startup command and run the whole demo once.
- [ ] Input files are ready and easy to find.
- [ ] Nothing private on screen: no `.env`, passwords, personal data or confidential figures.
- [ ] Fictional data is labelled "Fictional workshop data".
- [ ] Screen zoom is large enough to read from the back of the room.
- [ ] A backup run on the fictional sample is ready in case live input fails.
- [ ] One person presents and one drives; you have timed it at under five minutes.

Rules: everything shown must run, so no slides about what it would do. Do not claim features that do not exist. Say when data is fictional.

## Monday handover

Write `output/handover.md` with these headings. Keep it in `output/` because it may mention work material.

```markdown
# <Tool name>: handover

## What it does
One paragraph: who uses it, what goes in, what comes out.

## How to start it
Exact commands or clicks, from a fresh start.

## Inputs
Which files or sources, where they live, and who may use them.

## How we know it works
What correct looks like, and the checks we ran (only checks that actually ran).

## What the agent got wrong
From the PLAN.md table: what happened, how we noticed, what we changed.

## Known limits
What it does not do, and where a person must still check.

## Next improvement
The one change that would make it most useful.

## What we need
Access, budget, data permission or IT approval needed for real use.

## Owner
Who looks after it from Monday.
```
