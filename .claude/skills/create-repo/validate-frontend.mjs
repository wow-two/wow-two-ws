import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const root = resolve(process.argv[2] ?? '.');
const failures = [];
const requireFile = (path) => {
  if (!existsSync(join(root, path))) failures.push(`missing ${path}`);
};
const readManifest = (path) => {
  try {
    return JSON.parse(readFileSync(join(root, path), 'utf8'));
  } catch {
    failures.push(`unreadable package manifest: ${path}`);
    return {};
  }
};
const hasVueSource = (path) => existsSync(path) && readdirSync(path, { withFileTypes: true })
  .some((entry) => entry.isDirectory()
    ? hasVueSource(join(path, entry.name))
    : entry.name.endsWith('.vue'));

for (const path of [
  'pnpm-workspace.yaml', 'pnpm-lock.yaml', 'apps/web/index.html',
  'apps/web/vite.config.ts', 'apps/web/tsconfig.json',
]) requireFile(path);

// The starter uses explicit package globs; keep validation independent of installed npm dependencies.
if (existsSync(join(root, 'pnpm-workspace.yaml'))) {
  const yaml = readFileSync(join(root, 'pnpm-workspace.yaml'), 'utf8');
  const block = yaml.match(/^packages:\s*(?:#.*)?\r?\n((?:(?:[ \t]+.*)?\r?\n)*)/m)?.[1] ?? '';
  const flow = yaml.match(/^packages:\s*\[([^\]]*)\]/m)?.[1];
  const entries = flow === undefined
    ? block.split(/\r?\n/).map((line) => line.match(/^\s*-\s*(.*?)\s*(?:#.*)?$/)?.[1]).filter(Boolean)
    : flow.split(',').map((entry) => entry.trim());
  const patterns = entries.map((entry) => entry.replace(/^(['"])(.*)\1$/, '$2'));
  for (const pattern of ['apps/*', 'packages/*']) {
    if (!patterns.includes(pattern)) failures.push(`pnpm-workspace.yaml must declare the literal ${pattern} glob`);
  }
  if (patterns.some((pattern) => pattern.startsWith('!apps'))) {
    failures.push('the starter workspace must include every app');
  }
}

const workspace = readManifest('package.json');
const app = readManifest('apps/web/package.json');
if (workspace.private !== true) failures.push('workspace package must be private');
if (!/^pnpm@\d+\.\d+\.\d+(?:[-+].+)?$/.test(workspace.packageManager ?? '')) {
  failures.push('workspace packageManager must pin a pnpm version');
}
if (app.private !== true) failures.push('apps/web package must be private');
if (!/^@[^/]+\/web$/.test(app.name ?? '')) failures.push('app package name must be @{brand}/web');
for (const [label, manifest] of [['workspace', workspace], ['apps/web', app]]) {
  for (const name of ['dev', 'build', 'typecheck']) {
    if (typeof manifest.scripts?.[name] !== 'string' || !manifest.scripts[name].trim()) {
      failures.push(`${label} needs a ${name} script`);
    }
  }
  const dependencies = { ...manifest.dependencies, ...manifest.devDependencies };
  for (const name of ['react', 'react-dom', '@vitejs/plugin-react', '@vitejs/plugin-react-swc']) {
    if (name in dependencies) failures.push(`${label} retains the legacy React dependency ${name}`);
  }
}
const appDependencies = { ...app.dependencies, ...app.devDependencies };
for (const name of ['vue', 'vite', '@vitejs/plugin-vue']) {
  if (!(name in appDependencies)) failures.push(`apps/web must declare ${name}`);
}
if (!hasVueSource(join(root, 'apps/web/src'))) failures.push('apps/web/src has no Vue component');
if (existsSync(join(root, 'src'))) failures.push('application source remains at the workspace root');

if (failures.length > 0) {
  console.error(`[scaffold] frontend template/output is not conformant: ${root}`);
  for (const failure of failures) console.error(`  - ${failure}`);
  process.exitCode = 1;
} else {
  console.log(`[scaffold] Vue frontend workspace validated: ${root}`);
}
