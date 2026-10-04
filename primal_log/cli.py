import sys
import argparse
from .main import generate_changelog, get_git_commits

def main():
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="Primal-Log: changelog from conventional commits")
    p.add_argument("--repo", help="Path to git repo (default: cwd)")
    p.add_argument("--output", help="Output file path")
    a = p.parse_args()
    commits = get_git_commits(a.repo)
    if not commits:
        print("No commits found in repository")
        return
    generate_changelog(commits, a.output)

if __name__ == "__main__":
    main()
