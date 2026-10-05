// Mirror the workshop skills from .agents/skills (the maintained copy, read natively by Codex)
// into .claude/skills so Claude Code finds the same skills under the same names. Local files only.
// Edit .agents/skills/masterclass-*, then run this script. --check only reports drift (exit 1).
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const source = path.join(root, '.agents/skills');
const target = path.join(root, '.claude/skills');
const prefix = 'masterclass-';
const check = process.argv.includes('--check');

function files(directory, base = directory) {
  return readdirSync(directory).flatMap(entry => {
    const full = path.join(directory, entry);
    if (entry === '__pycache__' || entry === '.DS_Store') return [];
    return statSync(full).isDirectory() ? files(full, base) : [path.relative(base, full).split(path.sep).join('/')];
  }).sort();
}
function contents(directory) {
  return existsSync(directory) ? Object.fromEntries(files(directory).map(file => [file, readFileSync(path.join(directory, file))])) : {};
}
function same(a, b) {
  const keys = Object.keys(a);
  return keys.length === Object.keys(b).length && keys.every(key => b[key] && a[key].equals(b[key]));
}
const skills = dir => existsSync(dir) ? readdirSync(dir).filter(entry =>
  entry.startsWith(prefix) && existsSync(path.join(dir, entry, 'SKILL.md'))) : [];

const wanted = skills(source);
let drift = 0;
for (const skill of wanted) {
  const label = `.claude/skills/${skill}`;
  const want = contents(path.join(source, skill));
  const destination = path.join(target, skill);
  if (same(want, contents(destination))) { console.log(`UP TO DATE | ${label}`); continue; }
  drift++;
  if (check) { console.log(`DRIFT      | ${label} | differs from .agents/skills/${skill}`); continue; }
  rmSync(destination, { recursive: true, force: true });
  for (const [file, data] of Object.entries(want)) {
    mkdirSync(path.dirname(path.join(destination, file)), { recursive: true });
    writeFileSync(path.join(destination, file), data);
  }
  console.log(`SYNCED     | ${label}`);
}
for (const skill of skills(target).filter(skill => !wanted.includes(skill))) {
  drift++;
  if (check) { console.log(`STALE      | .claude/skills/${skill} | no source in .agents/skills`); continue; }
  rmSync(path.join(target, skill), { recursive: true, force: true });
  console.log(`REMOVED    | .claude/skills/${skill}`);
}
if (check && drift) {
  console.log('\nRun node scripts/sync-claude-skills.mjs to update the Claude Code copies.');
  process.exitCode = 1;
}
