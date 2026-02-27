#!/usr/bin/env python3
"""
Memory Janitor - Auto archive expired memories
P1: 90 days → archive
P2: 30 days → archive
"""
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path.home() / ".openclaw/workspace"
MEMORY_DIR = WORKSPACE / "memory"
ARCHIVE_DIR = MEMORY_DIR / "archive"

# TTL thresholds
P1_TTL = timedelta(days=90)
P2_TTL = timedelta(days=30)

def get_priority_and_age(file_path: Path):
    """Extract priority and age from memory file"""
    with open(file_path, 'r') as f:
        content = f.read(2000)  # Read first 2KB for metadata
    
    # Extract date from filename (YYYY-MM-DD.md)
    try:
        date_str = file_path.stem
        file_date = datetime.strptime(date_str, "%Y-%m-%d")
        age = datetime.now() - file_date
    except:
        return None, None
    
    # Check for priority tags
    priority = None
    if "[P0]" in content:
        priority = "P0"
    elif "[P1]" in content:
        priority = "P1"
    elif "[P2]" in content:
        priority = "P2"
    
    return priority, age

def cleanup():
    """Archive expired memories"""
    ARCHIVE_DIR.mkdir(exist_ok=True)
    
    archived = []
    for md_file in MEMORY_DIR.glob("*.md"):
        if md_file.name == "archive":
            continue
            
        priority, age = get_priority_and_age(md_file)
        
        if age and age > P2_TTL:
            dest = ARCHIVE_DIR / md_file.name
            shutil.move(str(md_file), str(dest))
            archived.append(f"{md_file.name} ({priority}, {age.days}d)")
    
    if archived:
        print(f"Archived {len(archived)} files:")
        for a in archived:
            print(f"  - {a}")
    else:
        print("No files to archive.")

if __name__ == "__main__":
    cleanup()
