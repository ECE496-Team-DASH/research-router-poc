import subprocess
import sys
from datetime import datetime

REPO_URL = "https://github.com/ECE496-Team-DASH/research-router-poc/"
FILES_OF_INTEREST = [
    "research_router_poc.ipynb", 
    "knowledge_graph.html",
    "knowledge_graph.png",
]
CHANGELOG = "CHANGELOG.md"

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python commit_and_changelog.py \"Your commit message here\"")
        sys.exit(1)
    msg = sys.argv[1]

    # Prepare changelog entry (no commit hash yet, will update after commit)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"## {timestamp}\n- Message: {msg}\n\n"

    # Prepend to CHANGELOG.md
    try:
        with open(CHANGELOG, 'r', encoding='utf-8') as f:
            old_content = f.read()
    except FileNotFoundError:
        old_content = ''
    with open(CHANGELOG, 'w', encoding='utf-8') as f:
        f.write(entry + old_content)

    # Stage all changes (including the updated changelog)
    run("git add .")

    # Commit
    run(f"git commit -m \"{msg}\"")

    # Get latest commit hash
    commit_hash = run("git rev-parse HEAD")
    commit_url = REPO_URL.rstrip('/') + f"/commit/{commit_hash}"

    # Build file URLs
    file_urls = []
    for fname in FILES_OF_INTEREST:
        file_urls.append(f"[{fname}]({REPO_URL.rstrip('/')}/blob/{commit_hash}/{fname})")

    # Update the top changelog entry with commit hash and file links
    updated_entry = f"## {timestamp}\n- Commit: [{commit_hash[:7]}]({commit_url})\n- Files: {', '.join(file_urls)}\n- Message: {msg}\n\n"
    with open(CHANGELOG, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace only the first entry (which we just wrote)
    content = content.replace(entry, updated_entry, 1)
    with open(CHANGELOG, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Changelog updated and commit created.\n{updated_entry}")

if __name__ == "__main__":
    main()
