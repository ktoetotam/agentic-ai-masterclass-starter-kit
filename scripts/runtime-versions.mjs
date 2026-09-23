import { readFileSync } from 'node:fs';

export const nodeTarget = readFileSync(new URL('../.node-version', import.meta.url), 'utf8').trim();
export const pythonTarget = readFileSync(new URL('../.python-version', import.meta.url), 'utf8').trim();

// Stay on the selected release series and reject prereleases and older patches.
export function meetsTarget(version, target, seriesParts) {
  if (!/^\d+\.\d+\.\d+$/.test(version) || !/^\d+\.\d+\.\d+$/.test(target)) return false;
  const actual = version.split('.').map(Number);
  const minimum = target.split('.').map(Number);
  if (!actual.slice(0, seriesParts).every((part, i) => part === minimum[i])) return false;
  for (let i = seriesParts; i < actual.length; i++) {
    if (actual[i] !== minimum[i]) return actual[i] > minimum[i];
  }
  return true;
}
