# Review behavior with realistic prompts

Use this procedure for new skills and substantial changes. Scale testing to the change: a wording correction needs focused review; a changed workflow or description needs realistic execution or selection tests. These are starter conventions informed by [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills), the system `skill-creator`, and [Anthropic's evaluation workflow](https://code.claude.com/docs/en/skills#run-evals-with-skill-creator). Consult the current official pages before adopting vendor-specific commands or formats.

## Choose cases and success criteria

- Start with a few realistic participant requests: a normal task, missing or invalid input, and a scope boundary. Add regression cases for demonstrated failures.
- Define observable success before running: expected artifacts, correct decisions, preserved files, accurate claims and permitted side effects. Check outcomes rather than exact wording, headings or a prescribed command sequence.
- For automatic selection, include both should-trigger requests and similar should-not-trigger requests. Do not name the skill in these prompts. An explicit `$skill` or `/skill` test proves execution, not automatic selection.
- Use synthetic fixtures. Save reusable prompts, fixture paths and expected outcomes with the maintained skill when useful. Do not add empty test directories to every skill.

## Run a fair comparison

- Snapshot the previous skill before a substantial revision. Compare the same requests against old and new versions; for a new skill, use no skill as the baseline.
- Use fresh isolated sessions and the same client, model, effort, tools, instructions and input files for each pair. Ensure the baseline cannot discover the candidate skill. A subagent inheriting a conversation that already contains the skill is not a clean no-skill baseline.
- Keep fixtures and mutations in a temporary workspace; put private reports and extracts in `output/`. Serve only browser assets in `public/`.
- Record the actual client/version, model and effort when available, skill revision, prompt, inputs, outputs, tool availability and limitations. Record duration and tokens only when the runtime provides them; never invent measurements.
- Repeat a case when variance or an unexplained failure matters. A few runs provide practical evidence, not a statistical guarantee.
- Evaluation does not authorize installing tools, paid API calls, sending, publishing or production changes. Use existing authorization and limits. Stop when a dependency, permission or agreed budget prevents a valid run; label simulated actions.
- Test Codex and Claude separately before claiming demonstrated compatibility. If one cannot run, report it as untested.

## Review and improve

- Use deterministic checks for verifiable results, and human review for clarity, usefulness and visual quality. Save pass/fail evidence and the actual artifacts. Do not rely only on the agent's claim that it succeeded.
- For complex or risky skills, use an independent evaluator where delegation is authorized. Provide only the realistic request, skill and necessary raw inputs, without the suspected bug, intended conclusion or proposed fix. Follow repository concurrency limits; no further delegation unless assigned.
- For subjective comparisons, hide which output is old or new where practical. Inspect transcripts when outputs suggest wasted work, unintended actions or hidden failures.
- Fix demonstrated weaknesses without tailoring the skill only to the test prompts. Keep at least one fresh request for a follow-up check. Retain useful regression cases.
- Report behavior checks separately from format, mirror, installation and activation checks. For each case give the result, evidence and remaining uncertainty; label checks not run and why. Do not declare a small test set proves universal reliability.

## Example authoring cases

Adapt these prompts and provide the required synthetic files before running. They are reusable examples, not a mandatory benchmark for every edit.

| Request | Expected observable behavior |
| --- | --- |
| Explain skills and plugins in this starter. Don't change anything. | Accurate explanation; no file changes, installation or activation. |
| Create a simple workshop skill called masterclass-meeting-summary that summarises fictional notes locally. | Maintained source and matching Claude copy; focused routing; no unrelated configuration or external actions. |
| Change one sentence in this existing workshop skill to clarify its output. | Focused edit; mirror updated; required repository checks reported; no unrelated changes. |
| Add a fictional challenge plugin with setup and summarise skills. | Both manifests and catalogues agree; package checks and isolated activation results reported accurately. |
| Build a landing page for a fictional bakery. | Authoring skill is not selected merely because the task involves a website; relevant website route used. |
| Create a plugin from these notes, but no notes are attached. | Missing input exposed; no fabricated extraction or unsupported success claim. |

Anthropic's skill-creator evaluation format and `claude plugin eval` format are distinct. Use the relevant current documentation if choosing either; this procedure does not require a particular evaluation runner.
