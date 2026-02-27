#!/usr/bin/env python3
"""
Memory Get Tool - Safe snippet read from memory files
Usage: python3 memory_get.py <file_path> [--from N] [--lines N]
"""
import sys
import argparse
from pathlib import Path

def read_snippet(file_path: str, from_line: int = 1, lines: int = 50):
    """Read safe snippet from memory file"""
    path = Path(file_path).expanduser()
    
    if not path.exists():
        print(f"File not found: {file_path}")
        return
    
    with open(path, 'r') as f:
        all_lines = f.readlines()
    
    total = len(all_lines)
    start = max(0, from_line - 1)
    end = min(total, start + lines)
    
    print(f"--- {path.name} (lines {start+1}-{end}/{total}) ---")
    for i, line in enumerate(all_lines[start:end], start + 1):
        print(f"{i:4d} | {line.rstrip()}")

def main():
    parser = argparse.ArgumentParser(description='Read memory file snippet')
    parser.add_argument('file_path', help='Path to memory file')
    parser.add_argument('--from', type=int, default=1, dest='from_line', help='Start line')
    parser.add_argument('--lines', type=int, default=50, help='Number of lines')
    args = parser.parse_args()
    
    read_snippet(args.file_path, args.from_line, args.lines)

if __name__ == "__main__":
    main()
