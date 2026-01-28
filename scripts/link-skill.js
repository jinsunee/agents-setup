const fs = require('fs');
const path = require('path');

const targetArg = process.argv[2];

if (!targetArg) {
  console.error('Usage: npm run link-skill <path-to-skill>');
  console.error('Example: npm run link-skill common/.agents/skills/browser-use');
  process.exit(1);
}

const fullPath = path.resolve(process.cwd(), targetArg);

if (!fs.existsSync(fullPath)) {
  console.error(`Error: Path does not exist: ${fullPath}`);
  process.exit(1);
}

const skillName = path.basename(fullPath);
const commonDir = path.resolve(process.cwd(), 'common');
const targetDirs = [
  path.join(commonDir, '.agent', 'skills'),
  path.join(commonDir, '.claude', 'skills')
];

targetDirs.forEach(dir => {
  if (!fs.existsSync(dir)) {
    console.log(`Creating directory: ${dir}`);
    fs.mkdirSync(dir, { recursive: true });
  }

  const linkPath = path.join(dir, skillName);
  
  // Use relative path for symlink
  const relativeTarget = path.relative(dir, fullPath);

  if (fs.existsSync(linkPath)) {
    const stats = fs.lstatSync(linkPath);
    if (stats.isSymbolicLink()) {
      console.log(`Removing existing symlink: ${linkPath}`);
      fs.unlinkSync(linkPath);
    } else {
      console.error(`Error: ${linkPath} exists and is not a symbolic link. Skipping.`);
      return;
    }
  }

  console.log(`Creating symlink: ${linkPath} -> ${relativeTarget}`);
  fs.symlinkSync(relativeTarget, linkPath);
});

console.log('Done!');
