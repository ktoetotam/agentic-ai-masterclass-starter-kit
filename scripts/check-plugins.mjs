// Check the skills, plugin manifests and marketplaces against the masterclass-plugin-authoring rules,
// so every skill and plugin works the same in Codex and Claude Code. Reads files only; exit 1 on a failure.
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const pluginsDir = path.join(root, '.agents/plugins/plugins');
const schema = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json';
const rootKeys = ['$schema', 'name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords', 'extensions'];
const shared = ['name', 'version', 'description', 'author', 'repository', 'keywords'];
const namePattern = /^(?!.*--)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
let failures = 0;

function report(problems, label) {
  if (problems.length) failures++;
  console.log(`${problems.length ? 'FAIL' : 'OK  '} | ${label}${problems.length ? ` | ${problems.join('; ')}` : ''}`);
}
function readJson(file, problems) {
  try { return JSON.parse(readFileSync(path.join(root, file), 'utf8')); }
  catch (error) { problems.push(`${file}: ${error.code === 'ENOENT' ? 'missing' : 'invalid JSON'}`); return null; }
}
const dirs = dir => existsSync(path.join(root, dir)) ? readdirSync(path.join(root, dir), { withFileTypes: true })
  .filter(entry => entry.isDirectory()).map(entry => entry.name).sort() : [];

// Plugin manifests: portable root plugin.json for Codex, .claude-plugin/plugin.json for Claude Code.
const plugins = dirs('.agents/plugins/plugins');
for (const plugin of plugins) {
  const base = `.agents/plugins/plugins/${plugin}`;
  const problems = [];
  const portable = readJson(`${base}/plugin.json`, problems);
  const claude = readJson(`${base}/.claude-plugin/plugin.json`, problems);
  if (existsSync(path.join(root, base, '.codex-plugin'))) problems.push('remove legacy .codex-plugin/');
  if (!existsSync(path.join(pluginsDir, plugin, 'skills'))) problems.push('no skills/ folder');
  if (portable) {
    if (portable.$schema !== schema) problems.push(`plugin.json $schema must be ${schema}`);
    for (const key of Object.keys(portable)) if (!rootKeys.includes(key)) problems.push(`plugin.json: key "${key}" is not allowed`);
    for (const key of Object.keys(portable.author || {})) if (!['name', 'email', 'url'].includes(key)) problems.push(`plugin.json: author.${key} is not allowed`);
    for (const key of ['version', 'description']) if (typeof portable[key] !== 'string') problems.push(`plugin.json: ${key} missing`);
    const prompts = portable.extensions?.['com.openai']?.interface?.defaultPrompt;
    if (prompts !== undefined && !(Array.isArray(prompts) && prompts.every(item => typeof item === 'string'))) problems.push('defaultPrompt must be a list of strings');
  }
  if (portable && claude) {
    for (const key of shared) if (JSON.stringify(portable[key]) !== JSON.stringify(claude[key])) problems.push(`${key} differs between the two manifests`);
  }
  const name = portable?.name ?? claude?.name;
  if (name !== plugin) problems.push(`manifest name "${name}" must equal folder "${plugin}"`);
  if (name && (!namePattern.test(name) || /^(claude|anthropic)/.test(name))) problems.push(`plugin name "${name}" is not allowed`);
  report(problems, `plugin ${plugin}`);
}

// Marketplaces: same plugins in both, paths from the repository root.
const marketProblems = [];
const codexMarket = readJson('.agents/plugins/marketplace.json', marketProblems);
const claudeMarket = readJson('.claude-plugin/marketplace.json', marketProblems);
const listed = { codex: [], claude: [] };
for (const [client, market, pathOf] of [
  ['codex', codexMarket, entry => entry.source?.source === 'local' ? entry.source.path : undefined],
  ['claude', claudeMarket, entry => entry.source]
]) {
  if (!market) continue;
  if (market.name !== 'ai-realist-workshops') marketProblems.push(`${client} marketplace name must stay ai-realist-workshops`);
  for (const entry of market.plugins || []) {
    listed[client].push(entry.name);
    const source = pathOf(entry);
    if (typeof source !== 'string' || !source.startsWith('./') || source.includes('..')) marketProblems.push(`${client} ${entry.name}: path must start with ./ and stay inside the repository`);
    else if (path.resolve(root, source) !== path.join(pluginsDir, entry.name)) marketProblems.push(`${client} ${entry.name}: path must be ./.agents/plugins/plugins/${entry.name}`);
  }
}
for (const plugin of plugins) {
  for (const client of ['codex', 'claude']) if (!listed[client].includes(plugin)) marketProblems.push(`${plugin} missing from the ${client} marketplace`);
}
if (listed.codex.join() !== listed.claude.join()) marketProblems.push('the two marketplaces must list the same plugins in the same order');
report(marketProblems, 'marketplaces');

// SKILL.md files: workshop skills, their Claude copies, activated copies and plugin skills.
const skillDirs = [
  ...dirs('.agents/skills').map(name => `.agents/skills/${name}`),
  ...dirs('.claude/skills').map(name => `.claude/skills/${name}`),
  ...plugins.flatMap(plugin => dirs(`.agents/plugins/plugins/${plugin}/skills`).map(name => `.agents/plugins/plugins/${plugin}/skills/${name}`))
];
for (const dir of skillDirs) {
  const problems = [];
  const file = path.join(root, dir, 'SKILL.md');
  if (!existsSync(file)) { report(['no SKILL.md'], dir); continue; }
  const text = readFileSync(file, 'utf8').replace(/\r\n/g, '\n');
  const front = text.match(/^---\n([\s\S]*?)\n---\n/);
  if (!front) { report(['no frontmatter between --- lines'], dir); continue; }
  const field = key => front[1].match(new RegExp(`^${key}:[ \\t]*(.*)$`, 'm'))?.[1].trim();
  const name = field('name');
  const description = field('description');
  const folder = path.basename(dir);
  if (name !== folder) problems.push(`name "${name}" must equal folder "${folder}"`);
  if (name && (name.length > 64 || !namePattern.test(name))) problems.push('name must be lowercase letters, digits and single hyphens, at most 64 characters');
  if (!description || ['|', '>'].includes(description[0])) problems.push('description must be one non-empty line');
  else {
    if (description.length > 1024) problems.push(`description is ${description.length} characters (limit 1024)`);
    if (!/^["']/.test(description) && /: /.test(description)) problems.push('description contains ": ", which breaks YAML');
    if (!/\bUse (when|whenever|before|after|first)\b/.test(description)) problems.push('description needs a "Use when ..." clause');
  }
  const lines = text.split('\n').length;
  if (lines > 500) problems.push(`SKILL.md has ${lines} lines (keep under 500)`);
  report(problems, dir);
}

console.log(failures ? `\n${failures} item(s) need attention. See .agents/skills/masterclass-plugin-authoring/SKILL.md.` : '\nAll skills, plugins and marketplaces follow the template.');
if (failures) process.exitCode = 1;
