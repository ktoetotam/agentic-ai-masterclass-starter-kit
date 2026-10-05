---
name: <folder-name>
description: <What it does, in one plain sentence with the concrete outputs> - <the main steps>. Use when someone <the words participants actually say>, or <the situation that should trigger it>.
---

# <Title in plain words>

<One or two sentences: what this skill produces and for whom. State the boundary - what it does not do and which skill does that instead.>

Read `AGENTS.md` first. Load these only when a step needs them:

- [references/<topic>.md](references/<topic>.md): <what is in it>.

## 1. <First step>

1. <Imperative instruction. Name the exact command, file or check.>
2. <Next instruction.>

## 2. <Next step>

- <Instruction.>

## Report

<What to show the participant: a table or short summary, the checks that actually ran, and one next step as a paste-ready message. Name skills the way the current client invokes them: `$name` in Codex, `/name` in Claude Code.>

## Boundaries

<What this skill never does without the concrete authorization in `AGENTS.md`: sending, publishing, paying, installing, reading `.env`. Do not report a check as passed unless it ran in this session.>
