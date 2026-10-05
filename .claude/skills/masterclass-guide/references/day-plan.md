# The day

Thursday 8 October 2026, Munich, 09:00–18:00 local time (Europe/Berlin). If the facilitator announces a different schedule, follow the facilitator.

## Agenda and what to push for

| Time | Block | What the guide pushes for |
| --- | --- | --- |
| Before | Optional online setup sessions | Tools installed and checked with `$masterclass-check`. |
| 09:00 | Introduction and goals | Nothing to build yet. |
| 09:20 | Chosen builds and suggested groups | Choose mode: agree one build per group and start PLAN.md. |
| 09:45 | Choosing tools: Claude Cowork, Claude Code and Codex | Note the group's tool choice in PLAN.md. |
| 10:25 | Tool check and setup | `$masterclass-check`, then `$masterclass-setup` for the chosen challenge's tools. |
| 10:45 | Build block one | Something of yours running on screen by lunch. Elegance can wait. |
| 12:30 | Lunch | Update the progress log; list blockers to fix after lunch. |
| 13:15 | Build block two: make it real | Your input, the features that matter, deploy if a link is needed. |
| 15:00 | Check-in | Show where you are, name the blockers, decide what you need to finish. |
| 15:30 | Build block three: finish and polish | One ambitious feature, then polish. Features freeze around 16:30. |
| 17:00 | Demos | Five minutes per group. Everything shown must run. |
| 17:45 | Conclusion | What you built, what you learned about agents, what to take back on Monday. |

## Checkpoints

- **12:30:** something runs on screen, even on sample data.
- **15:00:** the core works on real or representative input; blockers are written down.
- **16:30:** feature freeze; rehearse the demo.
- **17:00:** demo.

## Behind schedule? Cut in this order

1. Deployment: show it in the local preview.
2. Your own data: use the fictional sample and say so.
3. Extra features.
4. Design polish.

Never cut the check against "what correct looks like". A demo that shows how you checked the result beats a bigger demo that cannot be trusted.

## Group roles

| Role | What they do |
| --- | --- |
| Driver | Types messages to the agent and shares the screen. Rotate every block. |
| Checker | Tests results against "what correct looks like" and logs what the agent got wrong. |
| Data steward | Chooses and approves inputs; keeps private data out of Git, `public/` and the chat. |
| Integrator | Owns Git branches and merges, plus dependency files and the lockfile. |
| Storyteller | Keeps PLAN.md up to date and prepares the demo and the handover. |

With four people, combine data steward and storyteller. Several people can each run their own agent at the same time, as long as each one works on separate files; `masterclass-teamwork` describes how.
