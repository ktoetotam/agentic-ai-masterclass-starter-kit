# Bring your own problem: request triage fallback

This fictional example is available if you cannot bring work data.

**User:** an operations coordinator.

**Current task:** every Monday, review a table of requests, ask for missing details and assign an owner.

**Desired tool:** accept the input below, mark which requests are ready for review, draft clarification text for incomplete requests and export a status table. Keep the input unchanged. Nothing is sent.

| Request ID | Topic | Requested by | Consent to contact | Details |
| --- | --- | --- | --- | --- |
| R001 | Demo | alex@fern-sample.invalid | Yes | A 20-minute walkthrough for a team of 18 |
| R002 | Training | sam@cedar-demo.invalid | Yes | |
| R003 | Partnership | | No | Explore a joint fictional workshop |

**Success:** R001 is ready for human review; R002 is missing details; R003 is missing a contact and consent. A second run does not duplicate requests. The output clearly distinguishes drafts from delivered messages.

**Stretch goal:** let the coordinator adjust a status and see a change log. A local JSON file or SQLite database is enough. A CRM account is not required.
