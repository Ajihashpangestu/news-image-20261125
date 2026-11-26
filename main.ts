// News-image entry (Node 22, standard library only).
// Copies the prepared entry.png beside this file to the output directory.
// Deterministic: the same bytes are written on every run.
// Revision: v13 artwork (12 cards, larger lead scenes, larger briefs, CL confidence).

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
const dest = join(outDir, 'entry.png');
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
// v13: prepared artwork is byte-identical on every run.
