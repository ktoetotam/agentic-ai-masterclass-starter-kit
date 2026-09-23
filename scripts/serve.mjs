// Only public/ is served, only on this machine. Keep data and secrets outside it.
import { createServer } from 'node:http';
import { readFile, realpath, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadEnvFile } from 'node:process';

try { loadEnvFile(fileURLToPath(new URL('../.env', import.meta.url))); }
catch (error) { if (error.code !== 'ENOENT') throw error; }

const root = await realpath(fileURLToPath(new URL('../public', import.meta.url)));
const port = Number(process.env.PORT || 4173);
if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error('PORT must be 0–65535.');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
  '.mjs': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.mp3': 'audio/mpeg',
  '.mp4': 'video/mp4', '.pdf': 'application/pdf', '.woff2': 'font/woff2' };
const inside = file => file === root || file.startsWith(root + path.sep);
const server = createServer(async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405, { Allow: 'GET, HEAD' }).end(); return; }
  try {
    const urlPath = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    if (urlPath.split(/[\\/]/).some(part => part.startsWith('.'))) { res.writeHead(403).end(); return; }
    let file = path.resolve(root, '.' + urlPath);
    if (!inside(file)) { res.writeHead(403).end(); return; }
    if ((await stat(file)).isDirectory()) file = path.join(file, 'index.html');
    file = await realpath(file);
    if (!inside(file)) { res.writeHead(403).end(); return; }
    const body = await readFile(file);
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
    res.end(req.method === 'HEAD' ? undefined : body);
  } catch (error) {
    res.writeHead(error instanceof URIError ? 400 : 404).end('File not found');
  }
});
server.on('error', error => { console.error(`Preview could not start: ${error.message}. Try a different PORT.`); process.exitCode = 1; });
server.listen(port, '127.0.0.1', () => console.log(`Preview: http://127.0.0.1:${server.address().port} (Ctrl+C to stop)`));
