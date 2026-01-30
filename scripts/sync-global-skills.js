#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const homeDir = os.homedir();
const sourceDir = path.join(homeDir, '.agents', 'skills');

// Target directories for global skills
const targetDirs = [
  path.join(homeDir, '.claude', 'skills'),
  path.join(homeDir, '.gemini', 'antigravity', 'global_skills')
];

// Validate source directory exists
if (!fs.existsSync(sourceDir)) {
  console.error(`Error: Source directory does not exist: ${sourceDir}`);
  console.error('Please create ~/.agents/skills directory first.');
  process.exit(1);
}

console.log(`Syncing global skills from: ${sourceDir}`);
console.log('');

targetDirs.forEach(dir => {
  // Clear the target directory to ensure it only contains items from the current source
  if (fs.existsSync(dir)) {
    console.log(`Cleaning target directory: ${dir}`);
    fs.rmSync(dir, { recursive: true, force: true });
  }
  
  console.log(`Creating directory: ${dir}`);
  fs.mkdirSync(dir, { recursive: true });

  const items = fs.readdirSync(sourceDir);
  items.forEach(item => {
    const itemPath = path.join(sourceDir, item);
    // Only link directories (skills)
    if (fs.statSync(itemPath).isDirectory()) {
      const linkPath = path.join(dir, item);
      const relativeTarget = path.relative(dir, itemPath);
      
      console.log(`  Creating symlink: ${item} -> ${relativeTarget}`);
      fs.symlinkSync(relativeTarget, linkPath);
    }
  });
  console.log('');
});

console.log('✅ Global skills synced successfully!');
