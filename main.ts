// News-image entry (Node 22, standard library only).
// Copies the prepared entry.png beside this file to the output directory.
// Deterministic: the same bytes are written on every run.
// Revision: v6 artwork (50 stories, scene backdrops, colored map pins, tighter briefs).

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
const dest = join(outDir, 'entry.png');
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
