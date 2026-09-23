// Initialize the extracted workshop kit only. No staging, commits, remotes, or network calls.
import { appendFile, lstat, readFile, realpath } from 'node:fs/promises';
import { accessSync, constants, existsSync, realpathSync, statSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptFile = fileURLToPath(import.meta.url);
const projectName = 'agentic-ai-masterclass-starter';
const ignoreBlock = `# Masterclass team repository: keep local files private
.env
.env.*
!.env.example
.dev.vars*
*.pem
*.key
.venv/
node_modules/
.wrangler/
deployment-target.json
private/
output/
__pycache__/
*.log
.DS_Store
`;
const redirectedGitEnvironment = [
  'GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE',
  'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
  'GIT_CONFIG', 'GIT_CONFIG_COUNT', 'GIT_CONFIG_PARAMETERS', 'GIT_CEILING_DIRECTORIES',
];

export function supportsGit(version) {
  const match = /^git version (\d+)\.(\d+)\.(\d+)(?:[ .-]|$)/.exec(version.trim());
  if (!match || /(?:alpha|beta|rc)\d*/i.test(version)) return false;
  const [, major, minor] = match.map(Number);
  return major > 2 || (major === 2 && minor >= 55);
}

// Resolve first: executing /usr/bin/git on a Git-less Mac can open an installer.
export function resolveGitExecutable({ platform = process.platform, pathValue = process.env.PATH || '', run = spawnSync } = {}) {
  const gitName = platform === 'win32' ? 'git.exe' : 'git';
  const executable = pathValue.split(path.delimiter).filter(Boolean)
    .map(directory => path.resolve(directory.replace(/^"|"$/g, ''), gitName))
    .find(candidate => {
      try { accessSync(candidate, constants.X_OK); return statSync(candidate).isFile(); } catch { return false; }
    });
  if (!executable) throw new Error('Git is missing from PATH. Follow guides/setup-technical.md#install-git.');
  if (platform === 'darwin' && realpathSync(executable) === '/usr/bin/git') {
    const selected = run('/usr/bin/xcode-select', ['-p'], { encoding: 'utf8', timeout: 10000, windowsHide: true });
    const developerPath = selected.status === 0 ? selected.stdout?.trim() : null;
    if (!developerPath || !existsSync(path.join(developerPath, 'usr/bin/git'))) {
      throw new Error('The macOS Git installer shim is on PATH, but developer tools are unavailable. It was not run. Follow guides/setup-technical.md#install-git.');
    }
  }
  return executable;
}

function git(executable, root, args) {
  const result = spawnSync(executable, args, {
    cwd: root, encoding: 'utf8', windowsHide: true, timeout: 10000,
    env: { ...process.env, LC_ALL: 'C', GIT_TERMINAL_PROMPT: '0' },
  });
  if (result.error?.code === 'ETIMEDOUT') throw new Error('Git exceeded the 10-second timeout. Inspect the folder before retrying; no history was deleted.');
  if (result.error) throw new Error('Git could not start. Follow guides/setup-technical.md#install-git.');
  return { ...result, stdout: result.stdout.trim(), stderr: result.stderr.trim() };
}

function requireSuccess(result, action) {
  if (result.status !== 0) throw new Error(`${action} failed: ${result.stderr || 'Git returned an error.'}`);
  return result.stdout;
}

async function requirePlainPath(root, relative, directory = false) {
  const entry = await lstat(path.join(root, relative)).catch(() => null);
  if (!entry || entry.isSymbolicLink() || (directory ? !entry.isDirectory() : !entry.isFile())) {
    throw new Error(`Expected the standalone kit's ${relative}; it must not be a symlink.`);
  }
}

export async function initializeTeamRepo({ root, team }) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(team ?? '') || team.length > 40) {
    throw new Error('Use a team slug of 1–40 lowercase letters/digits separated by single hyphens, for example team-01.');
  }
  const redirected = redirectedGitEnvironment.filter(name => process.env[name] !== undefined);
  if (redirected.length) throw new Error(`Git location/configuration is overridden by ${redirected.join(', ')}. Use a normal terminal for this kit.`);
  root = await realpath(root);
  for (const file of ['package.json', 'AGENTS.md', '.gitignore', 'scripts/setup-team-repo.mjs']) await requirePlainPath(root, file);
  for (const directory of ['.agents', 'data', 'public', 'scripts']) await requirePlainPath(root, directory, true);
  const packageJson = JSON.parse(await readFile(path.join(root, 'package.json'), 'utf8'));
  if (packageJson.name !== projectName || packageJson.private !== true) throw new Error('This is not the standalone Agentic AI Masterclass kit.');
  const agents = await readFile(path.join(root, 'AGENTS.md'), 'utf8');
  if (!agents.startsWith('# Agentic AI Masterclass workspace')) throw new Error('The workshop workspace marker is missing.');
  const executable = resolveGitExecutable();
  const version = requireSuccess(git(executable, root, ['--version']), 'Checking Git');
  if (!supportsGit(version)) throw new Error(`Git 2.55.0 or newer is required; found ${version}. Follow guides/setup-technical.md#install-git.`);

  const ancestor = git(executable, path.dirname(root), ['rev-parse', '--show-toplevel']);
  if (ancestor.status === 0) throw new Error('This kit is inside another Git repository. Extract it outside the AI Realist website and all other repositories.');
  if (!ancestor.stderr.includes('not a git repository')) throw new Error('Could not establish that the kit is outside other repositories; no changes were made.');
  const repository = git(executable, root, ['rev-parse', '--show-toplevel']);
  const gitEntry = await lstat(path.join(root, '.git')).catch(() => null);
  if (repository.status === 0) {
    if (await realpath(repository.stdout) !== root) throw new Error('This kit is inside another Git repository. Extract it outside the AI Realist website and all other repositories.');
    if (!gitEntry?.isDirectory() || gitEntry.isSymbolicLink()) throw new Error('Linked worktrees and submodules are not initialized by this helper. Existing Git data has been preserved.');
    const assignedTeam = git(executable, root, ['config', '--local', '--get', 'masterclass.teamSlug']);
    if (assignedTeam.status !== 0) throw new Error('This folder is already a Git repository not created by this helper. Keep its history and use the clone/existing-repository instructions in guides/teamwork.md.');
    if (assignedTeam.stdout !== team) throw new Error(`This repository is already assigned to ${assignedTeam.stdout}; no changes were made.`);
    return { root, team, created: false, version };
  }
  if (gitEntry || !repository.stderr.includes('not a git repository')) throw new Error('Existing or inaccessible Git metadata was found. Resolve it without deleting history; no changes were made.');

  // All checks precede changes. Append to, rather than replace, participant rules.
  const ignorePath = path.join(root, '.gitignore');
  const existingIgnore = await readFile(ignorePath, 'utf8');
  if (!existingIgnore.includes(ignoreBlock)) {
    await appendFile(ignorePath, `${existingIgnore.endsWith('\n') ? '\n' : '\n\n'}${ignoreBlock}`);
  }
  requireSuccess(git(executable, root, ['-c', 'init.templateDir=', 'init', '--initial-branch=main']), 'Initializing the local repository');
  requireSuccess(git(executable, root, ['config', '--local', 'masterclass.teamSlug', team]), 'Recording the local team slug');
  return { root, team, created: true, version };
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 1 && args[0] === '--help') {
    console.log('Usage: node scripts/setup-team-repo.mjs --team team-01\nRun from the extracted kit root. Creates a local main branch only; no identity changes, staging, commits, remotes, or pushes.');
    return;
  }
  if (args.length !== 2 || args[0] !== '--team') throw new Error('Usage: node scripts/setup-team-repo.mjs --team team-01');
  const root = await realpath(path.join(path.dirname(scriptFile), '..'));
  if (await realpath(process.cwd()) !== root) throw new Error('Open a terminal in the extracted kit root before running this script.');
  const result = await initializeTeamRepo({ root, team: args[1] });
  console.log(`${result.created ? 'Created' : 'Preserved existing'} local team repository: ${result.team}\nFolder: ${result.root}\n${result.version}`);
  console.log('Nothing has been staged, committed, or published. Your Git identity, branches, and remotes were not changed in an existing repository.\nNext: follow guides/teamwork.md to review selected files, make the initial commit, and connect the approved private team repository.');
}

if (process.argv[1] && await realpath(process.argv[1]) === await realpath(scriptFile)) {
  main().catch(error => { console.error(`Team repository setup stopped: ${error.message}`); process.exitCode = 1; });
}
