import subprocess
import json
import os
import re
from datetime import datetime

def get_git_commits(repo_path=None):
    """Run 'git log --pretty=format' and parse commits"""
    try:
        cwd = repo_path or os.getcwd()
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H|%s|%an|%ad", "--date=short"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=cwd
        )
        if result.returncode != 0:
            return []
        lines = [line.strip() for line in result.stdout.split("\n") if line.strip()]
        commits = []
        for line in lines:
            parts = line.split("|")
            if len(parts) >= 4:
                commit_hash, subject, author, date = parts[0], parts[1], parts[2], parts[3]
                try:
                    dt = datetime.strptime(date, "%Y-%m-%d").date()
                except:
                    continue
                commits.append({
                    "hash": commit_hash,
                    "subject": subject,
                    "author": author,
                    "date": dt
                })
    except Exception as e:
        return []
    return commits

def parse_conventional_commit(subject):
    """Parse conventional commit format: feat: add login, fix: typo, etc."""
    if ":" not in subject:
        return "other", subject
    type_part, message = subject.split(":", 1)
    commit_type = type_part.strip().lower()
    return commit_type, message.strip()

def generate_changelog(commits, output_path=None):
    if not commits:
        return "No commits found"
    
    sections = {
        "Features": [],
        "Fixes": [],
        "Docs": [],
        "Breaking Changes": [],
        "Other": []
    }
    
    for commit in commits:
        commit_type, message = parse_conventional_commit(commit["subject"])
        if commit_type == "feat":
            sections["Features"].append(f"- {commit['subject']} ({commit['hash'][:7]})")
        elif commit_type == "fix":
            sections["Fixes"].append(f"- {commit['subject']} ({commit['hash'][:7]})")
        elif commit_type == "docs":
            sections["Docs"].append(f"- {commit['subject']} ({commit['hash'][:7]})")
        else:
            sections["Other"].append(f"- {commit['subject']} ({commit['hash'][:7]})")
    
    sections = {k: sorted(v) for k, v in sections.items()}
    
    lines = []
    lines.append("# Changelog\n")
    lines.append(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("\n## Features\n")
    lines.extend(sections["Features"])
    lines.append("\n## Fixes\n")
    lines.extend(sections["Fixes"])
    lines.append("\n## Docs\n")
    lines.extend(sections["Docs"])
    lines.append("\n## Breaking Changes\n")
    lines.extend(sections["Breaking Changes"])
    lines.append("\n## Other\n")
    lines.extend(sections["Other"])
    
    output = "\n".join(lines)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Changelog written to {output_path}")
    else:
        print(output)
    return output

def main():
    commits = get_git_commits()
    if not commits:
        print("No commits found in repository")
        return
    generate_changelog(commits)

if __name__ == "__main__":
    main()