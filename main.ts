// News-image entry (Node 22, standard library only).
// Copies the prepared entry.png beside this file to the output directory.
// Deterministic: the same bytes are written on every run.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
