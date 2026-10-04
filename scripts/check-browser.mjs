// Read-only, offline browser checks. Looks only at app locations, profile folder names and whether
// the two AI extension folders exist. Never reads browsing data, history, cookies or passwords.
import { spawnSync } from 'node:child_process';
import { existsSync, readdirSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const home = os.homedir();
const mac = process.platform === 'darwin';
const win = process.platform === 'win32';
const local = process.env.LOCALAPPDATA || path.join(home, 'AppData', 'Local');
const programFiles = [process.env.PROGRAMFILES, process.env['PROGRAMFILES(X86)']].filter(Boolean);

let failures = 0;
function report(ok, name, detail, required = true) {
  console.log(`${ok ? 'OK' : required ? 'NEEDS SETUP' : 'OPTIONAL'} | ${name} | ${detail}`);
  if (!ok && required) failures++;
}
function run(command, args) {
  const result = spawnSync(command, args, { encoding: 'utf8', timeout: 10000, windowsHide: true });
  return result.status === 0 ? result.stdout.trim() : null;
}
function list(directory) {
  try { return readdirSync(directory); } catch { return []; }
}
function newest(versions) {
  const parts = v => v.split(/[._]/).map(Number);
  return versions.filter(v => /^\d+(\.\d+)*(_\d+)?$/.test(v)).sort((a, b) => {
    const [x, y] = [parts(a), parts(b)];
    for (let i = 0; i < Math.max(x.length, y.length); i++) if ((x[i] || 0) !== (y[i] || 0)) return (x[i] || 0) - (y[i] || 0);
    return 0;
  }).at(-1);
}
function atLeast(version, minimum) {
  return newest([version, minimum]) === version || version.split('_')[0] === minimum;
}

const extensions = [
  { key: 'chatgpt', label: 'ChatGPT extension (OpenAI)', id: 'hehggadaopoacecdllhhajmbjkdcmajg', hosts: ['com.openai.codexextension'],
    store: 'https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg',
    connect: 'Codex connection: ChatGPT desktop app → Settings → Computer Use → Chrome → Install, until it shows Manage.' },
  { key: 'claude', label: 'Claude extension (Anthropic)', id: 'fcoeoabgfenejglbffodgkkbkcdhcgfn', hosts: ['com.anthropic.claude_code_browser_extension', 'com.anthropic.claude_browser_extension'],
    store: 'https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn', minimum: '1.0.36',
    connect: 'Claude connection: in Claude Code run claude --chrome once, restart Chrome, then /chrome shows Status: Enabled; or connect from the Claude desktop app.' }
];

const browsers = [
  { name: 'Google Chrome',
    apps: mac ? ['/Applications/Google Chrome.app', path.join(home, 'Applications/Google Chrome.app'), path.join(home, 'Desktop/Google Chrome.app')]
      : win ? [...programFiles, local].map(base => path.join(base, 'Google/Chrome/Application/chrome.exe'))
      : ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable'],
    data: mac ? path.join(home, 'Library/Application Support/Google/Chrome')
      : win ? path.join(local, 'Google/Chrome/User Data') : path.join(home, '.config/google-chrome'),
    registry: 'HKCU\\Software\\Google\\Chrome\\NativeMessagingHosts' },
  { name: 'Microsoft Edge',
    apps: mac ? ['/Applications/Microsoft Edge.app', path.join(home, 'Applications/Microsoft Edge.app')]
      : win ? programFiles.map(base => path.join(base, 'Microsoft/Edge/Application/msedge.exe'))
      : ['/usr/bin/microsoft-edge', '/usr/bin/microsoft-edge-stable'],
    data: mac ? path.join(home, 'Library/Application Support/Microsoft Edge')
      : win ? path.join(local, 'Microsoft/Edge/User Data') : path.join(home, '.config/microsoft-edge'),
    registry: 'HKCU\\Software\\Microsoft\\Edge\\NativeMessagingHosts' }
];

function appVersion(app) {
  if (mac) return run('/usr/bin/plutil', ['-extract', 'CFBundleShortVersionString', 'raw', path.join(app, 'Contents/Info.plist')]);
  if (win) return newest(list(path.dirname(app)));
  return null;
}
function hostInstalled(browser, hosts) {
  if (win) return hosts.some(host => run('reg', ['query', `${browser.registry}\\${host}`, '/ve']) !== null);
  return hosts.some(host => existsSync(path.join(browser.data, 'NativeMessagingHosts', `${host}.json`)));
}

for (const browser of browsers) {
  browser.app = browser.apps.find(existsSync);
  browser.version = browser.app ? appVersion(browser.app) : null;
  browser.profiles = list(browser.data).filter(name => name === 'Default' || /^Profile \d+$/.test(name));
  browser.found = {};
  for (const extension of extensions) {
    const profiles = browser.profiles.filter(profile => list(path.join(browser.data, profile, 'Extensions', extension.id)).length);
    const versions = profiles.flatMap(profile => list(path.join(browser.data, profile, 'Extensions', extension.id)));
    browser.found[extension.key] = profiles.length ? { profiles, version: newest(versions) } : null;
  }
}

const [chrome, edge] = browsers;
const edgeWithExtension = Boolean(edge.app && Object.values(edge.found).some(Boolean));
report(Boolean(chrome.app) || edgeWithExtension, 'Google Chrome',
  chrome.app ? `Installed${chrome.version ? ` (${chrome.version})` : ''}.`
    : edgeWithExtension ? 'Not installed; Microsoft Edge with an AI extension is used instead.'
    : 'Install it from https://www.google.com/chrome/ (Mac: drag it into Applications, or Home → Applications without an admin password).');

let anyExtension = false;
for (const browser of browsers.filter(b => b.app)) {
  for (const extension of extensions) {
    const found = browser.found[extension.key];
    if (found) anyExtension = true;
    report(Boolean(found), `${browser.name} · ${extension.label}`,
      found ? `Found in browser profile ${found.profiles.join(', ')}${found.version ? `; version ${found.version.split('_')[0]}` : ''}.`
        : `Not found. Install from ${extension.store} if you use this AI app.`, false);
    if (found && extension.minimum && found.version && !atLeast(found.version, extension.minimum)) {
      report(false, `${browser.name} · ${extension.label} version`,
        `Version ${found.version.split('_')[0]} is older than ${extension.minimum}; update it in chrome://extensions.`, false);
    }
  }
}
report(anyExtension, 'AI browser extension',
  anyExtension ? 'At least one AI browser extension is installed.'
    : 'Install the ChatGPT extension (for Codex) or the Claude extension (for Claude Code or Cowork). Links: guides/setup.md, step 3.');

for (const browser of browsers.filter(b => b.app)) {
  for (const extension of extensions.filter(e => browser.found[e.key])) {
    const connected = hostInstalled(browser, extension.hosts);
    report(connected, `${browser.name} · ${extension.label.split(' (')[0]} connection`,
      connected ? 'The agent-side connection is set up on this computer.' : extension.connect, false);
  }
}

console.log('\nManual checks: the extension is switched on in chrome://extensions and you are signed in to it in the browser profile you use.');
console.log('Codex: Settings → Computer Use shows Manage next to your browser. Claude Code: /chrome shows Status: Enabled and Extension: Installed.');
console.log(failures ? `\n${failures} required browser check(s) need attention.` : '\nBrowser checks passed. Finish the manual checks above.');
process.exitCode = failures ? 1 : 0;
