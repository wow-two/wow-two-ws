import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = dirname(fileURLToPath(import.meta.url));
const assets = readdirSync(join(root, 'dist/assets'));
const script = readFileSync(join(root, 'dist/assets', assets.find(name => name.endsWith('.js'))), 'utf8');
const css = readFileSync(join(root, 'dist/assets', assets.find(name => name.endsWith('.css'))), 'utf8');
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>First ten · WoW2 product lab</title><style>${css.replaceAll('</style', '<\\/style')}</style></head><body><div id="app"></div><script type="module">${script.replaceAll('</script', '<\\/script')}</script></body></html>`;
writeFileSync(join(root, 'prototype.html'), html);
console.log(`Portable prototype written: ${Buffer.byteLength(html)} bytes. No external assets.`);
