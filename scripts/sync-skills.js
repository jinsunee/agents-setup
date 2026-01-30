#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const targetArg = process.argv[2];

if (!targetArg) {
  console.error('Usage: sync-skills <path-to-skills-dir>');
  console.error('Example: sync-skills common/.agents/skills');
  process.exit(1);
}

const fullPath = path.resolve(process.cwd(), targetArg);

if (!fs.existsSync(fullPath)) {
  console.error(`Error: Path does not exist: ${fullPath}`);
  process.exit(1);
}

const skillBaseName = path.basename(fullPath);

// Find the base directory (where .agents lives)
let baseDir = null;
const parts = fullPath.split(path.sep);
const agentsPartIdx = parts.lastIndexOf('.agents');

if (agentsPartIdx !== -1) {
  baseDir = parts.slice(0, agentsPartIdx).join(path.sep) || path.sep;
} else {
  console.log('Note: ".agents" not found in path, using current directory as base.');
  baseDir = process.cwd();
}

const targetDirs = [
  path.join(baseDir, '.agent', 'skills'),
  path.join(baseDir, '.claude', 'skills')
];

console.log(`Syncing all skills from: ${fullPath}`);

targetDirs.forEach(dir => {
  // Clear the target directory to ensure it only contains items from the current source
  if (fs.existsSync(dir)) {
    console.log(`Cleaning target directory: ${dir}`);
    fs.rmSync(dir, { recursive: true, force: true });
  }
  
  console.log(`Creating directory: ${dir}`);
  fs.mkdirSync(dir, { recursive: true });

  const items = fs.readdirSync(fullPath);
  items.forEach(item => {
    const itemPath = path.join(fullPath, item);
    // Only link directories (skills)
    if (fs.statSync(itemPath).isDirectory()) {
      const linkPath = path.join(dir, item);
      const relativeTarget = path.relative(dir, itemPath);
      
      console.log(`Creating symlink: ${linkPath} -> ${relativeTarget}`);
      fs.symlinkSync(relativeTarget, linkPath);
    }
  });
});

console.log('Done!');
