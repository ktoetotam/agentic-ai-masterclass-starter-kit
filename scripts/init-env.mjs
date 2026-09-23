// Create a participant-local environment file without overwriting existing values.
import { copyFile, constants } from 'node:fs/promises';

try {
  await copyFile(new URL('../.env.example', import.meta.url), new URL('../.env', import.meta.url), constants.COPYFILE_EXCL);
  console.log('Created .env from the public-safe example. Edit it locally; keep it out of Git.');
} catch (error) {
  if (error.code !== 'EEXIST') throw error;
  console.log('Kept your existing .env unchanged.');
}
