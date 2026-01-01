import os
import fnmatch
import datetime

# Configuration
IGNORE_PATTERNS = [
    '.git', '__pycache__', 'node_modules', 'venv', '.venv', 'env', 
    'dist', 'build', '.DS_Store', '*.pyc', '*.pyo', '*.pyd', 
    '.vscode', '.idea', 'package-lock.json', 'yarn.lock', 
    '*.log', '.env', '.env.*',
    '*.png', '*.jpg', '*.jpeg', '*.gif', '*.ico',
    '*.woff', '*.woff2', '*.ttf', '*.eot', '*.svg', '*.mp4',
    'collect.py', 'codebase_dump_*.md', 'COMPLETE_PRODUCT_ROADMAP_V2.md' # Ignore self, previous dumps, and roadmap
]

def load_gitignore(root_dir):
    gitignore_path = os.path.join(root_dir, '.gitignore')
    if not os.path.exists(gitignore_path):
        return []
    
    patterns = []
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            patterns.append(line)
    return patterns

def should_ignore(path, root_dir, ignore_patterns):
    rel_path = os.path.relpath(path, root_dir)
    name = os.path.basename(path)
    
    # Split path to check each component against strict directory ignores
    parts = rel_path.split(os.sep)
    for part in parts:
        if part in ['.git', 'node_modules', 'venv', '.venv', '__pycache__', 'dist', 'build']:
            return True

    for pattern in ignore_patterns:
        # Normalize pattern
        clean_pattern = pattern.rstrip('/')
        
        # 1. Exact Name Match (e.g. .DS_Store)
        if fnmatch.fnmatch(name, clean_pattern):
            return True
            
        # 2. Path Match (e.g. backend/input_images/*.png)
        if fnmatch.fnmatch(rel_path, clean_pattern):
            return True
        
        # 3. Directory Match (if pattern implies a directory)
        # e.g. "backend/input_images/" should match "backend/input_images/foo.png"
        if pattern.endswith('/') or '/' in pattern:
             if rel_path.startswith(clean_pattern + os.sep) or rel_path == clean_pattern:
                 return True
                 
    return False

def collect_code(root_dir):
    # Output file in the parent folder (Project Root)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"codebase_dump_{timestamp}.md"
    output_path = os.path.join(root_dir, output_filename)
    
    ignore_patterns = IGNORE_PATTERNS + load_gitignore(root_dir)
    
    print(f"Collecting code from {root_dir}...")
    print(f"Output will be saved to {output_path}")

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# Codebase Dump - {timestamp}\n\n")
        outfile.write(f"Root: {root_dir}\n")
        outfile.write("Ignored: .git, node_modules, venv, binary files, etc.\n\n")
        
        # Traverse
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Modify dirnames in-place to skip ignored directories efficiently
            safe_dirs = []
            for d in dirnames:
                full_path = os.path.join(dirpath, d)
                if not should_ignore(full_path, root_dir, ignore_patterns):
                     safe_dirs.append(d)
            dirnames[:] = safe_dirs
            
            # Sort for consistent output
            dirnames.sort()
            filenames.sort()
            
            for f in filenames:
                full_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(full_path, root_dir)
                
                # Skip the output file itself
                if f == output_filename:
                    continue
                
                if should_ignore(full_path, root_dir, ignore_patterns):
                    continue
                
                # Setup markdown code block
                outfile.write(f"## File: {rel_path}\n\n")
                
                ext = os.path.splitext(f)[1].lower().replace('.', '')
                if not ext:
                    # Map some common no-extension files
                    if f in ['Dockerfile', 'Makefile']:
                        ext = 'dockerfile' if f == 'Dockerfile' else 'makefile'
                    else:
                        ext = 'txt'
                
                outfile.write(f"```{ext}\n")
                
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                        # Basic check for likely binary content if not filtered by extension
                        if '\0' in content: 
                            outfile.write("(Binary content detected, skipped)\n")
                        else:
                            outfile.write(content)
                except Exception as e:
                    outfile.write(f"Error reading file: {e}")
                
                outfile.write("\n```\n\n")
                
    print(f"Done. Successfully created {output_filename}")

if __name__ == "__main__":
    # Assume the script is run from the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    collect_code(current_dir)
