// Copy one challenge plugin's skills into this project so Codex (.agents/skills) and Claude Code
// (.claude/skills) find them in a new chat without installing a plugin. Local files only.
// A copy someone edited is kept unless --force is given.
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const pluginsDir = path.join(root, '.agents/plugins/plugins');
const targets = ['.agents/skills', '.claude/skills'];
const marker = '.activated.json';
const [name, ...flags] = process.argv.slice(2);
const force = flags.includes('--force');

const available = existsSync(pluginsDir) ? readdirSync(pluginsDir).filter(dir =>
  existsSync(path.join(pluginsDir, dir, 'skills'))) : [];
if (!name || name.startsWith('--')) {
  console.log(`Challenge plugins: ${available.join(', ') || 'none'}`);
  console.log('Usage: node scripts/activate-challenge.mjs <plugin> [--force]');
  process.exit(name === '--list' ? 0 : 1);
}
if (!available.includes(name)) {
  console.error(`Unknown challenge plugin "${name}". Available: ${available.join(', ') || 'none'}`);
  process.exit(1);
}

function files(directory, base = directory) {
  return readdirSync(directory).flatMap(entry => {
    const full = path.join(directory, entry);
    if (entry === marker || entry === '__pycache__' || entry === '.DS_Store') return [];
    return statSync(full).isDirectory() ? files(full, base) : [path.relative(base, full).split(path.sep).join('/')];
  }).sort();
}
function contents(directory, renameTo) {
  return Object.fromEntries(files(directory).map(file => {
    let data = readFileSync(path.join(directory, file));
    if (renameTo && file === 'SKILL.md') {
      data = Buffer.from(data.toString('utf8').replace(/^(---\r?\n[\s\S]*?^name:\s*).*$/m, `$1${renameTo}`));
    }
    return [file, data];
  }));
}
function fingerprint(map) {
  const hash = createHash('sha256');
  for (const [file, data] of Object.entries(map).sort()) hash.update(file).update('\0').update(data).update('\0');
  return hash.digest('hex');
}

const skillsDir = path.join(pluginsDir, name, 'skills');
let kept = 0;
const blocked = new Set();
for (const skill of readdirSync(skillsDir).filter(entry => existsSync(path.join(skillsDir, entry, 'SKILL.md')))) {
  const skillName = `${name}-${skill}`;
  const wanted = contents(path.join(skillsDir, skill), skillName);
  const wantedPrint = fingerprint(wanted);
  for (const target of targets) {
    const destination = path.join(root, target, skillName);
    const label = `${target}/${skillName}`;
    if (existsSync(destination)) {
      const current = fingerprint(contents(destination));
      let recorded = null;
      try { recorded = JSON.parse(readFileSync(path.join(destination, marker), 'utf8')).fingerprint; } catch { /* no marker */ }
      if (current === wantedPrint) { console.log(`UP TO DATE | ${label}`); continue; }
      if (current !== recorded && !force) {
        console.log(`KEPT       | ${label} | it was edited here; run with --force to replace it`);
        kept++;
        continue;
      }
    }
    try {
      if (existsSync(destination)) rmSync(destination, { recursive: true, force: true });
      for (const [file, data] of Object.entries(wanted)) {
        mkdirSync(path.dirname(path.join(destination, file)), { recursive: true });
        writeFileSync(path.join(destination, file), data);
      }
      writeFileSync(path.join(destination, marker), JSON.stringify({
        plugin: name, skill, fingerprint: wantedPrint, source: `.agents/plugins/plugins/${name}/skills/${skill}`
      }, null, 2) + '\n');
      console.log(`ACTIVATED  | ${label}`);
    } catch (error) {
      if (!['EPERM', 'EACCES', 'EROFS'].includes(error.code)) throw error;
      console.log(`BLOCKED    | ${label} | no permission to write here (${error.code})`);
      blocked.add(target);
    }
  }
}
console.log(`\nStart a new chat to use them: $${name}-<skill> in Codex, /${name}-<skill> in Claude Code.`);
if (kept) console.log(`${kept} edited cop${kept === 1 ? 'y was' : 'ies were'} kept unchanged.`);
if (blocked.size) {
  console.log(`\nBlocked: ${[...blocked].join(', ')}. Codex's sandbox protects the .agents folder. Run this command again with`);
  console.log('your approval to run it outside the sandbox; it only copies skill files inside this project.');
  process.exitCode = 2;
}
