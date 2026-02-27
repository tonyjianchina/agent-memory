#!/usr/bin/env python3
"""
Memory Compounding - Extract insights from daily logs
Analyzes memory files and generates L1 insights
"""
import os
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.home() / ".openclaw/workspace"
MEMORY_DIR = WORKSPACE / "memory"
INSIGHTS_DIR = WORKSPACE / "insights"
LESSONS_FILE = WORKSPACE / "lessons" / "lessons.jsonl"

def analyze_logs():
    """Analyze recent logs for patterns"""
    recent_files = sorted(MEMORY_DIR.glob("*.md"), reverse=True)[:7]
    
    if not recent_files:
        print("No recent logs found.")
        return
    
    print(f"Analyzing {len(recent_files)} recent log files...")
    
    # Extract key events/patterns
    events = []
    for f in recent_files:
        with open(f, 'r') as file:
            content = file.read()
            # Simple extraction - look for lines with specific patterns
            for line in content.split('\n'):
                if '【' in line and '】' in line:  # Tagged entries
                    events.append(line.strip())
    
    return events

def generate_insight(events: list):
    """Generate monthly insight file"""
    INSIGHTS_DIR.mkdir(exist_ok=True)
    
    month = datetime.now().strftime("%Y-%m")
    insight_file = INSIGHTS_DIR / f"{month}.md"
    
    content = f"""# Insights - {month}

## Key Events
"""
    for e in events[:20]:
        content += f"- {e}\n"
    
    content += f"""
---

*Generated: {datetime.now().isoformat()}*
"""
    
    with open(insight_file, 'w') as f:
        f.write(content)
    
    print(f"Generated insight: {insight_file}")

def main():
    events = analyze_logs()
    if events:
        generate_insight(events)
    else:
        print("No events to extract.")

if __name__ == "__main__":
    main()
