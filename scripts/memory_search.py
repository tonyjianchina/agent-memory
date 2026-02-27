#!/usr/bin/env python3
"""
Memory Search Tool - Semantic search across memory files
Usage: python3 memory_search.py <query> [--limit N]
"""
import os
import sys
import json
import argparse
from pathlib import Path

MEMORY_DIR = Path.home() / ".openclaw/workspace/memory"
MEMORY_FILE = Path.home() / ".openclaw/workspace/MEMORY.md"

def search_keyword(query: str, limit: int = 5):
    """Simple keyword search in memory files"""
    results = []
    
    # Search MEMORY.md
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, 'r') as f:
            content = f.read()
            if query.lower() in content.lower():
                results.append({
                    'file': str(MEMORY_FILE),
                    'snippet': content[:500],
                    'score': content.lower().count(query.lower())
                })
    
    # Search daily logs
    if MEMORY_DIR.exists():
        for md_file in sorted(MEMORY_DIR.glob("*.md"), reverse=True)[:30]:
            with open(md_file, 'r') as f:
                content = f.read()
                if query.lower() in content.lower():
                    results.append({
                        'file': str(md_file),
                        'snippet': content[:500],
                        'score': content.lower().count(query.lower())
                    })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]

def main():
    parser = argparse.ArgumentParser(description='Search memory files')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', type=int, default=5, help='Max results')
    args = parser.parse_args()
    
    results = search_keyword(args.query, args.limit)
    
    if not results:
        print("No results found.")
        return
    
    for i, r in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"File: {r['file']}")
        print(f"Snippet:\n{r['snippet'][:300]}...")

if __name__ == "__main__":
    main()
