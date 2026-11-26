// News-image entry (Node 22, standard library only).
// Copies the prepared entry.png beside this file to the output directory.
// Deterministic: the same bytes are written on every run.
// Revision: v5 artwork (50 stories, richer scenes, per-brief sure tags).

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, 'entry.png'));
