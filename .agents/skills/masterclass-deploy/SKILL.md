---
name: masterclass-deploy
description: Prepare and deploy an Agentic AI Masterclass project to its assigned Cloudflare workshop Worker, with explicit account, resource, and public-file checks.
---

# Deploy the masterclass project

Use the user's chosen project and existing authorization. Preparing a build or a dry run does not itself authorize publication. If the current request or earlier session instructions authorize deployment to the assigned target, carry it out after preflight without asking again. Do not create accounts, invite members, buy services, change DNS, or provision extra resources as a side effect.

## Establish the target

Read this project's facilitator-issued `deployment-target.json`, `wrangler.workshop.json`, optional `DEPLOYMENT.md`, package scripts, and build entry points. The target must identify a real assigned account and existing Worker; the human card can additionally record the intended URL, expiry, and approval. Unfilled placeholders are not a valid target. If the target is missing, finish the local build and explain exactly which account/name information is required. Do not synthesize an allowlist from a cached login or copy the config into an allowlist to make a check pass.

Use the standalone participant workspace, not the AI Realist website repository. The production account and Workers `airealist`, `airealist-dev`, and `airealist-api` are excluded from this workshop workflow. Never infer the intended target from a cached login or a parent directory's Wrangler configuration. A name prefix or environment is not a permissions boundary.

## Preflight

1. Present the exact account ID, Worker name, expected URL when supplied, config path, public directory, routes, and binding names/IDs. Never display credentials or secret values. Check environment overrides by name without dumping the whole environment; conflicting account, `CLOUDFLARE_ENV`, config redirection, or build-generated settings must be resolved to the approved target before proceeding.
2. Require the approved account and Worker name to match the config. The starter requires a separate workshop account, `workers_dev: true`, `routes: []`, and no custom domains. No production domains (`airealist.org`, `airealist.net`, `airealist.uk`, `hypefree.ai`) or their subdomains. Do not add permissions or remove safeguards to overcome an authorization error.
3. Review the actual files that will be published. This starter permits static assets only in `public/`; if a build system outputs elsewhere, copy only its reviewed public build into `public/`. Exclude credentials, local `.env`/`.dev.vars`, source datasets containing personal information, installation receipts, and repository internals. Do not set the asset directory to `.`.
4. The bundled starter supports static assets only and deliberately rejects Worker scripts and bindings. For a requested dynamic app, prepare local code and a facilitator-reviewed separate project; preserve the starter guard. Editable Worker code can reach its bindings and secrets, so a scoped deployment token does not make production bindings safe. Bind only sanctioned workshop resources, keep secrets server-side, and apply the agreed authentication and usage limits. Do not auto-provision resources or enable remote bindings as a repair step.
5. Use the project's pinned Wrangler and lockfile. The base starter has no dependencies; for the optional deployment track, install the workshop-selected version with `npm install --save-dev --save-exact wrangler@4.137.0` and preserve the generated lockfile. If a prepared lockfile already exists, use `npm ci` after reviewing package scripts. On Windows PowerShell use `npm.cmd`/`npx.cmd` when script policy blocks the `.ps1` launchers. Build and test the user-visible behavior locally. Run `node scripts/check-deploy.mjs` and then `npx --no-install wrangler deploy --config wrangler.workshop.json --dry-run`. A dry run checks the build, not remote permissions. Never bypass or weaken a failed guard.

## Authentication and deployment

Current granular Worker permissions require an **account-owned API token** scoped to Editor on the assigned existing Worker. `wrangler login` OAuth does not support granular authorization as documented on 23 September 2026. The facilitator supplies the scoped token privately and an expiry. Do not read unrelated stored personal credentials or copy tokens into chat or tracked source files. The participant stores the scoped `CLOUDFLARE_API_TOKEN` and assigned `CLOUDFLARE_ACCOUNT_ID` in this project’s ignored `.env` using a local editor. Both Wrangler and the starter guard load that file. Check presence and scope without printing values.

Existing process variables can override `.env`; resolve conflicts before publishing. Do not ask the participant to paste credentials into the conversation or persist them globally. For dynamic Worker projects, `.env` contains local application variables and deployed values use Worker secrets; avoid exposing deployment credentials as application bindings.

Use explicit configuration for every Wrangler operation:

```text
node scripts/check-deploy.mjs
npx --no-install wrangler deploy --config wrangler.workshop.json
```

Run the commands separately and proceed to deploy only if the guard succeeds. Recheck after loading credentials because the account environment variable can conflict with the target.

Deploy once the target, scope, and publication authorization are established. On a permission or account mismatch, stop the remote attempt and report the specific mismatch; complete remaining local work. Do not retry with a different account, broader role, production config, or a new Worker name. Prefer facilitator deployment if granular authorization is unavailable.

Verify the returned URL matches the card, open it, and check the core interaction. Report the URL, tests performed, and remaining limitations. Distinguish a successful dry run from an actual deployment. Note the supplied expiry/cleanup time; token revocation does not remove a running deployment.

## Reference for changing provider behavior

Consult current official docs before changing commands or the permission model:

- [Granular roles and Wrangler token authentication](https://developers.cloudflare.com/workers/authorization/)
- [Worker roles and binding permissions](https://developers.cloudflare.com/workers/authorization/workers/)
- [Wrangler deployment commands](https://developers.cloudflare.com/workers/wrangler/commands/workers/#deploy)
- [Wrangler environment variables](https://developers.cloudflare.com/workers/wrangler/system-environment-variables/)
- [Static asset configuration](https://developers.cloudflare.com/workers/static-assets/binding/)

The companion workspace guide `guides/facilitator-cloudflare.md` contains facilitator provisioning and local `.env` instructions; it may live outside a downloaded standalone starter. The essential checks above remain self-contained when that guide is unavailable.
