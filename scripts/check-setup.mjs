// Read-only, offline checks. No installs, environment changes, or account requests.
import { spawnSync } from 'node:child_process';
import { accessSync, constants, existsSync, realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { nodeTarget, pythonTarget, meetsTarget } from './runtime-versions.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
let failures = 0;
function report(ok, name, detail, required = true) {
  console.log(`${ok ? 'OK' : required ? 'NEEDS SETUP' : 'OPTIONAL'} | ${name} | ${detail}`);
  if (!ok && required) failures++;
}
function run(command, args) {
  const result = spawnSync(command, args, { cwd: root, encoding: 'utf8', timeout: 10000, windowsHide: true });
  return result.status === 0 ? result.stdout.trim() : null;
}
report(meetsTarget(process.versions.node, nodeTarget, 1), 'Node.js',
  `${process.version}; September 2026 target: ${nodeTarget}+ within Node 26 (Current). See guides/setup-technical.md.`);
// npm's JavaScript entrypoint avoids PowerShell execution-policy issues with npm.ps1.
const npmCandidates = [
  path.join(path.dirname(process.execPath), 'node_modules/npm/bin/npm-cli.js'),
  path.resolve(path.dirname(process.execPath), '../lib/node_modules/npm/bin/npm-cli.js')
];
const npmCLI = npmCandidates.find(existsSync);
const npmVersion = npmCLI ? run(process.execPath, [npmCLI, '--version']) : null;
report(Boolean(npmVersion), 'npm', npmVersion || 'Use the official Node distribution with npm included.');
// Resolve Git without executing macOS's developer-tools installer shim.
const gitName = process.platform === 'win32' ? 'git.exe' : 'git';
const gitPath = (process.env.PATH || '').split(path.delimiter).filter(Boolean)
  .map(directory => path.join(directory.replace(/^"|"$/g, ''), gitName))
  .find(candidate => {
    try { accessSync(candidate, constants.X_OK); return true; } catch { return false; }
  });
let gitVersion = null;
if (gitPath) {
  const appleShim = process.platform === 'darwin' && realpathSync(gitPath) === '/usr/bin/git';
  const developerPath = appleShim ? run('/usr/bin/xcode-select', ['-p']) : null;
  if (!appleShim || (developerPath && existsSync(path.join(developerPath, 'usr/bin/git')))) {
    gitVersion = run(gitPath, ['--version']);
  }
}
const gitParts = gitVersion?.match(/^git version (\d+)\.(\d+)\.(\d+)(?:\s|$|\.windows\.\d+$)/);
const gitOK = Boolean(gitParts && (Number(gitParts[1]) > 2 ||
  (Number(gitParts[1]) === 2 && Number(gitParts[2]) >= 55)));
report(gitOK, 'Git', gitOK ? gitVersion :
  `${gitVersion || 'Missing or unavailable on PATH'}; install current Git 2.55.0+ using guides/setup-technical.md#install-git. No GitHub account needed.`);
const python = path.join(root, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
const pyResult = existsSync(python) ? run(python, ['-c',
  'import json,sys,sqlite3,ssl; print(json.dumps({"version":list(sys.version_info[:3]),"releaselevel":sys.version_info.releaselevel,"sqlite":sqlite3.sqlite_version,"tls":bool(ssl.OPENSSL_VERSION)}))'
]) : null;
let py;
try { py = JSON.parse(pyResult); } catch { /* human-readable failure below */ }
const pyVersion = Array.isArray(py?.version) ? py.version.join('.') : 'unavailable';
const pyOK = meetsTarget(pyVersion, pythonTarget, 2) && py.releaselevel === 'final' && py.tls;
report(Boolean(pyOK), 'Project Python', pyOK ? `${py.version.join('.')}; SQLite ${py.sqlite}; TLS available` :
  `${pyVersion}; need stable Python ${pythonTarget}+ within Python 3.14. Follow guides/setup-technical.md; preserve any existing environment.`);
const poetryVersion = run('poetry', ['--version']);
const poetryParts = poetryVersion?.match(/Poetry \(version (\d+)\.(\d+)\.(\d+)\)/);
const poetryOK = Boolean(poetryParts && Number(poetryParts[1]) === 2 &&
  (Number(poetryParts[2]) > 5 || (Number(poetryParts[2]) === 5 && Number(poetryParts[3]) >= 1)));
report(poetryOK, 'Poetry', poetryOK ? poetryVersion : 'Install Poetry 2.5.1+ (2.x) using guides/setup-technical.md#poetry-and-env.');
const poetryEnvironment = poetryOK ? run('poetry', ['env', 'info', '--path']) : null;
let projectEnvironment = false;
try { projectEnvironment = Boolean(poetryEnvironment && realpathSync(poetryEnvironment) === realpathSync(path.join(root, '.venv'))); }
catch { /* missing/incomplete environment is reported below */ }
report(projectEnvironment, 'Poetry environment', projectEnvironment ? 'Poetry selects this project’s .venv.' :
  'Poetry must select this project’s .venv. Follow guides/setup-technical.md#poetry-and-env; preserve other environments.');
report(poetryOK && run('poetry', ['check', '--lock']) !== null, 'Python lockfile',
  'pyproject.toml and poetry.lock must agree. Use Poetry to add/remove dependencies and commit both files.');
report(Boolean(pyOK && run(python, [path.join(root, 'scripts/check-python.py')])), 'Python dependencies',
  'Run poetry install from this project to install the locked packages.');
report(existsSync(path.join(root, '.env')), 'Local configuration', 'Run node scripts/init-env.mjs once; keep .env out of Git.');
for (const file of ['AGENTS.md', '.agents/skills/masterclass-setup/SKILL.md', 'public/index.html', 'poetry.toml', '.env.example']) {
  report(existsSync(path.join(root, file)), file, 'Starter file');
}
report(Boolean(run('uv', ['--version'])), 'uv on PATH', 'Only needed to manage Python; an existing .venv can run without it.', false);
console.log('\nManual checks: sign in to ChatGPT; open Codex in this folder; see $masterclass-setup; open the preview; confirm your subscription and company policy.');
console.log('This check cannot verify sign-in, remaining AI usage, network access, reimbursement, or deployment permissions.');
console.log(failures ? `\n${failures} required check(s) need attention.` : '\nLocal runtime checks passed. Finish the manual checks before the workshop.');
process.exitCode = failures ? 1 : 0;
