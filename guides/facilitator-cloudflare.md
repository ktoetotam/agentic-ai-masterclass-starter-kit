# Cloudflare workshop deployment — facilitator runbook

Verified against Cloudflare documentation on **23 September 2026**. This is a preparation plan; no accounts, invitations, tokens, or deployments have been created by preparing this workspace.

## Recommended arrangement

Create a separate **AI Realist Workshops** Cloudflare account owned by AI Realist, with no production domains, customer data, production storage, or production credentials. Use one pre-created Worker per team, with its `workers.dev` address. Start with static assets. Give each team its own short-lived, account-owned API token with **Editor on that individual Worker**. Keep account administration and resource creation with the facilitator.

Cloudflare introduced individual Worker permissions in September 2026. Editor can update an existing Worker but cannot create or delete Workers. Granular Wrangler authorization currently requires an account-owned API token; `wrangler login` OAuth does not support it. These facts supersede older advice that all Worker deployment permissions must be account-wide. [Workers authorization](https://developers.cloudflare.com/workers/authorization/), [launch announcement](https://developers.cloudflare.com/changelog/post/2026-09-15-granular-worker-permissions/).

The separate account is still useful: Worker deployment permission also permits deployment with resource bindings without separate direct permissions on those resources. A name prefix, a Git branch, a Pages preview, a Wrangler environment, and a different URL are **not** account security boundaries. Treat every secret or dataset made available to editable workshop code as accessible to its editors. Separate accounts per team are preferable if teams must not be able to reach each other's data; otherwise put only shared, synthetic workshop data in the workshop account. [Binding authorization](https://developers.cloudflare.com/workers/authorization/#bindings).

Do not substitute the website's `wrangler.dev.jsonc`: it shares production KV, D1, and R2 resources. The existing production Workers include `airealist`, `airealist-dev`, and `airealist-api`. These are deny targets for workshop deployment. The production domains include `airealist.org`, `airealist.net`, `airealist.uk`, and `hypefree.ai`, including their `www` names. Do not copy their configuration, bindings, credentials, routes, or asset root into participant projects. The local guard checks a fingerprint of the production account ID without distributing the ID; Cloudflare permissions remain the real access boundary.

## Choose an operating mode

| Mode | Who deploys | When to use it |
| --- | --- | --- |
| AI Realist workshop account, individual Worker tokens | Each team | Preferred shared workshop arrangement; synthetic data only. |
| AI Realist workshop account, facilitator deployment | Facilitator | Scoped token or invitation setup is unavailable, or a project needs central secrets. Teams submit a reviewed build. |
| Participant's separate personal free account | Participant | Independent fallback when the workshop account is not ready. Keep the app static and use `workers.dev`; no domain purchase is required. |
| AI Realist production account | Facilitator only | Exceptional fallback after review; participants receive no account-wide deployment credentials. Prefer staying local until the separate account is ready. |

Pages' documented API permission remains account-scoped `Pages Write`; the reviewed docs do not establish a per-project Pages token equivalent to per-Worker Editor. Use Workers Static Assets for direct participant deployment. Do not hand out a shared Pages or legacy Workers edit token. [API permissions](https://developers.cloudflare.com/fundamentals/api/reference/permissions/), [Pages API](https://developers.cloudflare.com/pages/configuration/api/).

## Prepare before the session

1. **Create the workshop account and assign ownership.** Use an AI Realist-controlled owner and a backup facilitator, with MFA. Record the account ID and a responsible person. Keep participants out of billing, account settings, API-token administration, DNS, zone administration, and Worker product-wide roles.
2. **Reserve a `workers.dev` subdomain.** For example, `airealist-workshops` if available. The actual issued subdomain is authoritative; do not promise the example hostname. Add no production zones or custom domains.
3. **Pre-create team Workers.** Naming convention: `amc-YYYYMMDD-team-01`, `amc-YYYYMMDD-team-02`, and so on. Use the actual event date. The facilitator deploys an empty/static starting page first because individual Worker grants apply only to existing Workers. Set `workers_dev: true`, `preview_urls: false`, `routes: []`, and no bindings or schedules. No participant needs permission to create Workers. [Worker roles](https://developers.cloudflare.com/workers/authorization/workers/).
4. **Create one account-owned token per team or participant.** In the workshop account, go to **Manage Account → Account API Tokens → Create Token**. Choose **Workers → Editor**, scope it to the assigned existing Worker only, and set an expiry for the end of the workshop plus the announced grace period. Recommended local convention: 24 hours after the final session. Review the summary before creation. Do not choose Workers Platform Admin, Developer Platform Admin, all Workers, Pages Write, DNS Edit, Workers Routes Write, or token-management permissions. Record the token label and expiry, never the token value, in the facilitator roster. [Account API tokens](https://developers.cloudflare.com/fundamentals/api/get-started/account-owned-tokens/).
5. **Optionally invite dashboard users.** From the assigned Worker's **Invite** button, grant individual Worker **Editor**. This requires a Super Administrator to send the invitation. A dashboard invitation is optional for CLI-only use and does not replace the scoped API token. Check that existing group or account roles do not add broader rights. [Worker invitations](https://developers.cloudflare.com/changelog/post/2026-09-21-invite-members-to-workers/).
6. **Distribute privately.** Give each team its account ID, Worker name, URL, scope, expiry, and token through an individual secure channel. Never project a token on screen or paste it into a Codex conversation, shared document, repository, browser JavaScript, or the `public/` folder. Account IDs and Worker names are not secrets.
7. **Rehearse the exact flow on a test identity.** Deploy the assigned static Worker, verify its URL, and inspect the token policy. In the workshop account, prepare a second harmless test Worker and confirm that the participant identity/token cannot read its source or deploy to it. Use a reviewed negative test against that disposable Worker, never a write probe against production. Verify the selected account is not the production account above, and that the participant's grants exclude it entirely. A local dry run validates a build; it does not prove remote authorization.

If the current dashboard cannot issue the resource-scoped grant described in the documentation, use facilitator-only deployment. Do not widen permissions to get past an error.

## Deployment card for each team

Fill this in before distributing the workspace. Keep credentials elsewhere.

```text
Account display name: AI Realist Workshops
Approved account ID: <actual workshop account ID>
Existing Worker name: <actual amc-YYYYMMDD-team-NN name>
Expected URL: https://<worker>.<actual-subdomain>.workers.dev
Configuration: wrangler.workshop.json
Public assets folder: public/
Allowed bindings: none (or an explicit reviewed workshop-only list)
Token label: <label only>
Token expires at: <timestamp including timezone>
Deployment authorized by: <facilitator / session instruction>
Project removal date: <announced date>
```

The starter's deployment guard reads the facilitator-issued, gitignored `deployment-target.json` allowlist, with exactly the actual values below:

```json
{
  "account_id": "REPLACE_WITH_APPROVED_WORKSHOP_ACCOUNT_ID",
  "worker_name": "REPLACE_WITH_ASSIGNED_WORKER_NAME"
}
```

An optional `DEPLOYMENT.md` can hold the human-readable card above. Neither local file is a Cloudflare authorization mechanism: the token policy enforces the Worker permission. Do not invent the account ID, Worker name, or approval. The starter guard requires a separate account, static assets, and no bindings; a production-account or dynamic deployment must use a separately reviewed facilitator project, not a weakened starter guard.

## Participant commands: static project

Work in the standalone participant project, not the AI Realist website repository. The local exercises do not need Wrangler. When you reach deployment, install this workshop's selected version inside the project, without a global install or administrator rights:

```text
npm install --save-dev --save-exact wrangler@4.137.0
```

Wrangler **4.137.0** is the current stable npm release checked on 23 September 2026 ([official releases](https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.137.0)). Keep the resulting `package-lock.json`. On subsequent machines or a prepared project with that lockfile, use `npm ci`. In Windows PowerShell, use **`npm.cmd` and `npx.cmd`** in place of `npm` and `npx` in the commands below if script execution policy blocks the `.ps1` launcher; no policy change is needed. The facilitator should retest the selected Wrangler version before the event.

Set the supplied values in `wrangler.workshop.json` and keep them consistent with the facilitator-issued `deployment-target.json`:

```json
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "REPLACE_WITH_ASSIGNED_WORKER_NAME",
  "account_id": "REPLACE_WITH_APPROVED_WORKSHOP_ACCOUNT_ID",
  "compatibility_date": "2026-09-23",
  "workers_dev": true,
  "preview_urls": false,
  "routes": [],
  "assets": { "directory": "./public" }
}
```

No `main` file or remote bindings are needed for a static site. Put only the intended public site inside `public/`: never use the repository root as the assets directory. The starter guard permits only `public/`; if a build system outputs elsewhere, copy the reviewed public build into `public/`. [Static Assets configuration](https://developers.cloudflare.com/workers/static-assets/binding/).

Local check, with no Cloudflare login required:

```text
npx --no-install wrangler dev --config wrangler.workshop.json --local
```

Open the local URL Wrangler prints; stop with Ctrl+C. Run the starter's guard, then check the deploy bundle. Continue only when the guard passes:

```text
node scripts/check-deploy.mjs
npx --no-install wrangler deploy --config wrangler.workshop.json --dry-run
```

The dry run does not publish the app and does not check token scope. Inspect its output and the configuration: exact assigned account and name, no routes, no unapproved bindings, only intended public files. [Wrangler deployment commands](https://developers.cloudflare.com/workers/wrangler/commands/workers/#deploy).

When the facilitator supplies the deployment card and scoped token, add these variables to your ignored **`.env`** in a local text editor. Replace the placeholders privately; never paste a real token into chat, a command argument, or a tracked file.

```dotenv
CLOUDFLARE_ACCOUNT_ID=REPLACE_WITH_ASSIGNED_WORKSHOP_ACCOUNT_ID
CLOUDFLARE_API_TOKEN=REPLACE_WITH_YOUR_SCOPED_WORKSHOP_TOKEN
```

Both Wrangler and the starter guard load root `.env`. Existing terminal environment values can override it; resolve any conflicting account or environment override before proceeding. Use the root `.env` for this static exercise, with no `--env` flag. [Wrangler environment variables](https://developers.cloudflare.com/workers/wrangler/system-environment-variables/).

After the facilitator has authorized publication, run the guard again and continue only when it passes. Then publish (use `npx.cmd` in Windows PowerShell if necessary):

```text
node scripts/check-deploy.mjs
npx --no-install wrangler deploy --config wrangler.workshop.json
```

Check the resulting URL against the assigned `workers.dev` URL and test the intended behavior. If authorization fails, check expiry and the assignment with the facilitator. Do not repair it by switching to an owner credential, running `wrangler login`, broadening permissions or provisioning new resources.

After the session, remove the deployment token from your local `.env`. The facilitator must revoke it separately; removing the local copy does not revoke access or take down the published site.

## Dynamic apps and model APIs

The default workshop deployment is static and public. It can display example data and call no private API. A ChatGPT subscription does not supply API credit or make a browser-side model key safe.

For a dynamic exercise, the facilitator prepares a separate project with a server-side Worker, a separate model-provider project and workshop-only key, an exact resource list, a usage budget, and a shutdown time. The bundled static starter deliberately rejects Worker scripts and resource bindings: keep that guard intact. Any API key belongs in a Worker secret, never in client code or a `VITE_*` variable. Use an ignored `.env` beside the separate project’s Wrangler configuration for local development. Do not also create `.dev.vars`: Cloudflare loads it instead of `.env` when both exist. Keep deployment credentials out of this dynamic app’s runtime variables. Set the deployed secret from an interactive terminal with the matching configuration in the separately approved project, for example:

```text
npx --no-install wrangler secret put OPENAI_API_KEY --config wrangler.workshop.json
```

This command changes remote state and is only for an already authorized dynamic project. Anyone able to deploy that Worker can deploy code that reads its secrets; use a team-specific limited key, or keep deployment with the facilitator. [Worker secrets](https://developers.cloudflare.com/workers/configuration/secrets/).

For KV, D1, R2, Queues, service bindings, Durable Objects, or Workers AI, create only explicitly requested workshop resources and record their identifiers in the deployment card. Do not assume a separate binding or environment isolates underlying data. Keep local development local; `remote: true`, `--remote`, and Workers AI can use actual services. Add authentication and enforce request/rate and model-token limits before exposing a billable model endpoint publicly. CORS alone is not authentication. Do not copy a production service binding or connect to the website's API.

## Cost ownership and cleanup

Start with the free static path. The facilitator owns workshop Cloudflare charges; participants do not need to purchase a domain or a paid Cloudflare plan for this path. Consult current [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/) before enabling a paid feature.

For paid exercises, set a written workshop budget, alert thresholds, and a named person watching usage during the session. Configure **Manage Account → Billing → Billable Usage → Create budget alert** where available. Alerts notify; they do not stop usage. Set a CPU-time limit for dynamic Workers where supported, and enforce model-provider budgets separately. A CPU limit is not a total spending cap. [Budget alerts](https://developers.cloudflare.com/billing/manage/budget-alerts/), [Worker limits](https://developers.cloudflare.com/workers/platform/limits/).

At the announced end time:

- Revoke the issued tokens and remove individual Worker member/group grants. An API token expiry does not remove dashboard membership.
- Revoke workshop model keys, stop schedules and queue consumers, and disable billable public endpoints.
- Export participants' permitted source files before deleting anything they were promised they could retain.
- At the agreed retention date, delete the exact workshop Workers and resources from the roster, then inspect billing and usage again. Do not use a broad prefix-based deletion script across accounts.
- Record completion and any remaining paid subscriptions or stored data. Revoking a deployment token does not remove the already deployed app.

This runbook establishes the design and the commands. Account creation, resource provisioning, invitations, credential delivery, and public deployment remain facilitator preparation tasks until actually performed and verified.
