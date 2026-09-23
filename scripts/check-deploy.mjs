// A local mistake detector, NOT an authorization boundary. Cloudflare permissions
// and the separate workshop account enforce access. This script never deploys.
import { readFile, readdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { loadEnvFile } from 'node:process';
import { createHash } from 'node:crypto';
import path from 'node:path';
const root = fileURLToPath(new URL('../', import.meta.url));
// Compare a fingerprint without distributing the production account identifier.
const productionAccountFingerprint = '804ac09b83b87fbd9531aa9c1acb8c7a6d40f8f22a9c7db56fc1968d5cb71cb8';
const isProductionAccount = id => createHash('sha256').update(id).digest('hex') === productionAccountFingerprint;
const fail = message => { throw new Error(message); };
try {
  // Wrangler also reads root .env; check those overrides without printing values.
  try { loadEnvFile(path.join(root, '.env')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  const config = JSON.parse(await readFile(path.join(root, 'wrangler.workshop.json'), 'utf8'));
  const target = JSON.parse(await readFile(path.join(root, 'deployment-target.json'), 'utf8'));
  if (!/^[a-f0-9]{32}$/.test(target.account_id) || isProductionAccount(target.account_id)) fail('A separate workshop account is required.');
  if (!/^amc-[a-z0-9][a-z0-9-]{1,50}$/.test(target.worker_name)) fail('Use the existing amc- Worker assigned by the facilitator.');
  if (config.account_id !== target.account_id || config.name !== target.worker_name) fail('Config does not match the facilitator-issued deployment target.');
  if (process.env.CLOUDFLARE_ACCOUNT_ID && process.env.CLOUDFLARE_ACCOUNT_ID !== target.account_id) fail('CLOUDFLARE_ACCOUNT_ID conflicts with the target.');
  if (process.env.CLOUDFLARE_ENV) fail('Remove the CLOUDFLARE_ENV override for this standalone static configuration.');
  const allowed = new Set(['name', 'account_id', 'compatibility_date', 'workers_dev', 'preview_urls', 'routes', 'assets', '$schema']);
  if (Object.keys(config).some(key => !allowed.has(key))) fail('Only the static starter configuration is approved. Review backend/binding changes with the facilitator.');
  if (config.workers_dev !== true || config.preview_urls !== false || !Array.isArray(config.routes) || config.routes.length) fail('Use workers.dev, no routes or additional preview URLs.');
  if (config.assets?.directory !== './public' || Object.keys(config.assets).length !== 1) fail('Assets must be exactly ./public.');
  const publicDir = path.join(root, 'public');
  const files = [];
  async function walk(dir) {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      if (entry.isSymbolicLink()) fail('Symlinks are not allowed in public/.');
      if (entry.name.startsWith('.') || /^(AGENTS\.md|package.*\.json|.*\.(pem|key)|wrangler.*)$/i.test(entry.name)) fail('Private or configuration file found in public/.');
      const file = path.join(dir, entry.name);
      if (entry.isDirectory()) await walk(file);
      else files.push(path.relative(publicDir, file));
    }
  }
  await walk(publicDir);
  console.log(`Static deployment target: ${config.account_id} / ${config.name}\nPublic files (${files.length}):\n${files.join('\n')}`);
  console.log('\nLocal guard passed. Review every public file for private content. This does not verify Cloudflare token scope or authorize publication.');
  console.log('Next: follow guides/facilitator-cloudflare.md for the scoped token, local Wrangler dry run, and authorized deployment.');
} catch (error) {
  console.error(`Deployment blocked: ${error.message}\nRead guides/facilitator-cloudflare.md. Do not use the AI Realist website configuration.`);
  process.exitCode = 1;
}
